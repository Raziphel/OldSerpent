
#* Discord
from discord.ext.commands import command, Cog, Greedy
from discord import Member, DiscordException

import utils
# * Additions
from discord import Member, DiscordException
from discord.ext.commands import command, Cog, Greedy

from asyncio import sleep, Task
from datetime import datetime, timedelta
from typing import Tuple, Dict, Optional

import utils


class Muting(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temporary_mutes: Dict[int, Tuple[Task, datetime]] = {}
        self.bot.loop.create_task(self.bootstrap())


    @property  #! The welcome logs
    def server_logs(self):
        return self.bot.get_channel(self.bot.config['channels']['server'])


    async def bootstrap(self):
        '''Temp-Mute bootstrap!  Sexy Af!'''
        await self.bot.wait_until_ready()

        async with self.bot.database() as db:
            temp_mutes = await db('SELECT * FROM tempmute_timeout')
            if temp_mutes:
                for mute in temp_mutes:
                    expiration = mute['unmute_time']
                    guild = self.bot.get_guild(self.bot.config['garden_id'])
                    member = guild.get_member(mute['user_id'])

                    if member is None:
                        continue  #! User left the server.

                    task = self.create_temp_gag_task(member, expiration)
                    self.temporary_mutes[member.id] = (task, expiration)








    @Cog.listener()
    async def on_member_join(self, member):
        '''Catches jail breakers~!'''

        guild = member.guild

        mod = utils.Moderation.get(member.id)
        if mod.muted == True: #! Checks to make sure they were muted!
            prisoner = utils.DiscordGet(guild.roles, id=1028881308006502400)
            await member.add_roles(prisoner)

            await self.server_logs.send(embed=utils.LogEmbed(type="negative", title=f"Prisoner Tried to escape...", desc=f"{member} Was thrown back into the dungeons."))






    @utils.is_admin_staff()
    @command()
    async def ban(self, ctx, user:Greedy[Member], *, reason:Optional[str]="[No Reason Given]"):
        '''Bans any given amount of members given!'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)

        #! Ban for each given user!
        for i in user:
            #! Ban hammer message
            await i.send(F"**Sorry, you were banned from {ctx.guild} for: {reason}**\nHonestly man thats a rip...\nI doubt you will be missed tho! c:")
            await ctx.guild.ban(i, delete_message_days=1, reason=f'{reason} :: banned by {ctx.author!s}')

        #! Report who has been banned!
        if len(user) == 1:
            await ctx.send(embed=utils.WarningEmbed(title=f"Banned `{i}`."))
        else:
            await ctx.send(embed=utils.WarningEmbed(title=f"Banned `{len(user)}` users."))
        for i in user:
            await self.server_logs.send(embed=utils.LogEmbed(type="negative", author=f"User Banned", desc=f"{i.name} was banned!\n**By: {ctx.author}\nReason :: {reason}**"))




    @utils.is_admin_staff()
    @command(aliases=['g', 'pg', 'mute'])
    async def gag(self, ctx, user:Greedy[Member], *, reason:Optional[str]="[No Reason Given]"):
        '''Applies the prisoner role to a user or users'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)

        muted_role = utils.DiscordGet(ctx.guild.roles, id=1028881308006502400)

        #? check if it's a purge gag!
        if ctx.message.content.startswith('.pg'):
            try:
                await ctx.channel.purge(limit=100, check=lambda message: message.author.id == user.id)
            except: pass

        #! Add the role to the user
        for i in user:
            await i.add_roles(muted_role, reason=f'{reason} :: muted by {ctx.author.mention}')
            try:
                await member.edit(mute=False)
            except DiscordException: pass
            try: #? Tell them they are muted!
                await i.send(f'You were permanently muted for reason `{reason}`')
            except DiscordException:
                pass

        #! Send message to the channel
        if len(user) == 1:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} muted {user[0].mention} permenantly!", guild=ctx.guild))
        else:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} muted `{len(user)}` users!", guild=ctx.guild))

        #!Save to the DB
        for i in user:
            mod = utils.Moderation.get(i.id)
            mod.muted = True
        async with self.bot.database() as db:
            await mod.save(db)

        for i in user:
            await self.server_logs.send(embed=utils.LogEmbed(type="negative", title=f"User Muted", desc=f"{i.name} was muted!\nBy: **{ctx.author}**\nReason :: **{reason}**"))




    @utils.is_admin_staff()
    @command(aliases=['unmute'])
    async def ungag(self, ctx, user:Greedy[Member], *, reason:Optional[str]="[No Reason Given]"):
        '''Removes the prisoner role to a user or users'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)
            muted_role = utils.DiscordGet(ctx.guild.roles, id=1028881308006502400)
            await user.remove_roles(muted_role, reason='Mute removed.')
            await i.remove_roles(muted_role, reason=f'{reason} :: muted removed by {ctx.author.mention}')

        #! Send message to the channel
        if len(user) == 1:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} un-muted {user[0].mention}!", guild=ctx.guild))
        else:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} un-muted `{len(user)}` users!", guild=ctx.guild))

        #!Save to the DB
        for i in user:
            mod = utils.Moderation.get(i.id)
            mod.muted = False
        async with self.bot.database() as db:
            await mod.save(db)

        for i in user:
            await self.server_logs.send(embed=utils.LogEmbed(type="negative", title=f"User Un-Gagged", desc=f"{i.name} was un-muted!\nBy: **{ctx.author}**\nReason :: **{reason}**"))






    async def handle_mute_expiration(self, member:Member):
        muted_role = utils.DiscordGet(member.guild.roles, id=1028881308006502400)
        await member.remove_roles(muted_role, reason='Temp-mute expired.')

        try:
            await member.edit(mute=False)
        except DiscordException: pass

        try:
            del self.temporary_mutes[member.id]
        except KeyError: pass

        await self.server_logs.send(embed=utils.LogEmbed(type="positive", title=f"User un-muted", desc=f"{member.mention} was ungagged!\n\n**Temp-mute Has Expired!**"))

        #! Database Update!
        mod = utils.Moderation.get(member.id)
        mod.gagged = False
        async with self.bot.database() as db:
            await mod.save(db)
            await db('DELETE FROM tempmute_timeout WHERE user_id = $1', member.id)





    def create_temp_gag_task(self, member:Member, expiration:datetime):
        coro = utils.run_at(expiration, self.handle_mute_expiration, member)
        task = self.bot.loop.create_task(coro)
        self.temporary_mutes[member.id] = (task, expiration)
        return task





    @utils.is_admin_staff()
    @command(aliases=['tg', 'tmute', 'tempmute', 'tm'])
    async def tempgag(self, ctx, user:Greedy[Member], duration:utils.TimeConverter, *, reason:str="[No Reason Given]"):
        '''Temporarily applies the prisoner role to a user or users'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)

        muted_role = utils.DiscordGet(ctx.guild.roles, id=1028881308006502400)

        #! Add the role to the user
        for i in user:
            await i.add_roles(muted_role, reason=f'{reason} :: temp muted by {ctx.author.mention}')
            try: #? Tell them they are muted!
                await i.send(f'You were temporarily muted for `{duration}` seconds for reason: `{reason}`.')
            except DiscordException:
                pass

        #! Send message to the channel!
        if len(user) == 1:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} muted {user[0].mention} for {duration} seconds!", guild=ctx.guild))
        else:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} muted `{len(user)}` users  for {duration} seconds!", guild=ctx.guild))

        #!Save to the DB
        for i in user:
            mod = utils.Moderation.get(i.id)
            mod.gagged = True
            async with self.bot.database() as db:
                await mod.save(db)
                mute_expiration = datetime.now() + timedelta(seconds=duration)
                await db('INSERT INTO tempmute_timeout VALUES ($1, $2) '
                                'ON CONFLICT (user_id) '
                                'DO UPDATE SET unmute_time = $2', i.id, mute_expiration)
                self.create_temp_gag_task(i, mute_expiration)

        for i in user:
            await self.server_logs.send(embed=utils.LogEmbed(type="negative", title=f"User Gagged", desc=f"{i.name} was gagged!\nBy: **{ctx.author}**\nReason :: **{reason}**\nDuration :: **{duration}**"))






def setup(bot):
    x = Muting(bot)
    bot.add_cog(x)