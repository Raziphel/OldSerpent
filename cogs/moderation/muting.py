
#* Discord
from discord.ext.commands import command, Cog, Greedy
from discord import Member, Message, User, DiscordException

#* Additions
from asyncio import sleep, Task
from datetime import datetime, timedelta
from typing import Tuple, Dict, Optional

import utils

class Muting(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.temporary_mutes: Dict[int, Tuple[Task, datetime]] = {}
        self.bot.loop.create_task(self.bootstrap())


    async def bootstrap(self):
        '''Temp-Mute bootstrap!  Sexy Af!'''
        await self.bot.wait_until_ready()

        async with self.bot.database() as db:
            temp_mutes = await db('SELECT * FROM tempmute_timeout')
            if temp_mutes:
                for mute in temp_mutes:
                    expiration = mute['unmute_time']
                    guild = self.bot.get_guild(self.bot.config['guilds']['FurryRoyaleID'])
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
        if mod.prisoner == True: #! Checks to make sure they were muted!
            try: #! Get the guilds muted role
                for role in ctx.guild.roles:
                    if role.id in self.bot.muted_roles:
                        role_id = role.id
                await member.add_roles(prisoner)
            except: return

            log = await utils.ChannelFunction.get_log_channel(guild=member.guild, log="member")
            await log.send(embed=utils.LogEmbed(type="negative", title=f"Prisoner Tried to escape...", desc=f"{member} Was thrown back into the dungeons."))






    @utils.is_admin_staff()
    @command()
    async def ban(self, ctx, user:Greedy[Member], *, reason:Optional[str]="[No Reason Given]"):
        '''Bans any given amount of members given!'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)

        for i in user: 
            if any([r for r in i.roles if r.id in self.bot.nsfw_staff]):
                return await ctx.send(embed=utils.WarningEmbed(desc="Staff are unable to be banned!  Please demote first!", guild=ctx.guild))

        #! Ban for each given user!
        for i in user:
            #! Ban hammer message
            await i.send(F"**Sorry, you were banned from {ctx.guild} for: {reason}**\nHonestly man thats a rip...\nI doubt you will be missed tho! c:")
            await ctx.guild.ban(i, delete_message_days=1, reason=f'{reason} :: banned by {ctx.author!s}')

        #! Report who has been banned!
        if len(user) == 1:
            await ctx.send(embed=utils.WarningEmbed(warning=f"Banned `{i}`."))
        else:
            await ctx.send(embed=utils.WarningEmbed(warning=f"Banned `{len(user)}` users."))
        log = await utils.ChannelFunction.get_log_channel(guild=ctx.guild, log="member")
        for i in user:
            await log.send(embed=utils.LogEmbed(type="negative", author=f"User Banned", desc=f"{i.name} was banned!\n**By: {ctx.author}\nReason :: {reason}**"))




    @utils.is_nsfw_staff()
    @command(aliases=['g', 'pg'])
    async def gag(self, ctx, user:Greedy[Member], *, reason:Optional[str]="[No Reason Given]"):
        '''Applies the prisoner role to a user or users'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)

        for i in user: 
            if any([r for r in i.roles if r.id in self.bot.nsfw_staff]):
                return await ctx.send(embed=utils.WarningEmbed(desc="Staff are unable to be gagged!", guild=ctx.guild))

        try: #! Get the guilds muted role
            for role in ctx.guild.roles:
                if role.id in self.bot.muted_roles:
                    role_id = role.id
        except: return
        if role_id is None: #? Error in Config!
            return await ctx.send("Looks like this guild's muted roles can not be found in my config.", delete_after=15)

        muted_role = utils.DiscordGet(ctx.guild.roles, id=role_id)

        #? check if it's a purge gag!
        if ctx.message.content.startswith('.pg'):
            try:
                await ctx.channel.purge(limit=100, check=lambda message: message.author.id == member.id)
            except: pass

        #! Add the role to the user
        for i in user:
            await i.add_roles(muted_role, reason=f'{reason} :: gagged by {ctx.author.mention}')
            try: #? Tell them they are gagged!
                await i.send(f'You were permanently gagged for reason `{reason}`')
            except DiscordException:
                pass

        #! Send message to the channel
        if len(user) == 1:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} gagged {user[0].mention} permenantly!", guild=ctx.guild))
        else:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} gagged `{len(user)}` users!", guild=ctx.guild))

        #!Save to the DB
        for i in user:
            mod = utils.Moderation.get(i.id)
            mod.gagged = True
            mod.violations += 1
        async with self.bot.database() as db:
            await mod.save(db)

        log = await utils.ChannelFunction.get_log_channel(guild=ctx.guild, log="member")
        for i in user:
            await log.send(embed=utils.LogEmbed(type="negative", title=f"User Gagged", desc=f"{i.name} was gagged!\nBy: **{ctx.author}**\nReason :: **{reason}**"))




    @utils.is_nsfw_staff()
    @command(aliases=['unmute'])
    async def ungag(self, ctx, user:Greedy[Member], *, reason:Optional[str]="[No Reason Given]"):
        '''Removes the prisoner role to a user or users'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)


        #! Remove the roles from the users
        role_ids = []
        try: #! Get the guilds muted role
            for role in member.guild.roles:
                if role.id in self.bot.muted_roles:
                    role_ids.append(role.id)
        except: pass

        if role_ids is None:
            return

        for i in user:
            try: #? Get any muted roles to remove!
                for role_id in role_ids:
                    muted_role = utils.DiscordGet(member.guild.roles, id=role_id)
                    await member.remove_roles(muted_role, reason='Gag removed.')
            except DiscordException: pass
            await i.remove_roles(muted_role, reason=f'{reason} :: gag removed by {ctx.author.mention}')

        #! Send message to the channel
        if len(user) == 1:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} un-gagged {user[0].mention}!", guild=ctx.guild))
        else:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} un-gagged `{len(user)}` users!", guild=ctx.guild))

        #!Save to the DB
        for i in user:
            mod = utils.Moderation.get(i.id)
            mod.gagged = False
        async with self.bot.database() as db:
            await mod.save(db)

        log = await utils.ChannelFunction.get_log_channel(guild=ctx.guild, log="member")
        for i in user:
            await log.send(embed=utils.LogEmbed(type="negative", title=f"User Un-Gagged", desc=f"{i.name} was un-gagged!\nBy: **{ctx.author}**\nReason :: **{reason}**"))






    async def handle_mute_expiration(self, member:Member):
        role_ids = []
        try: #! Get the guilds muted role
            for role in member.guild.roles:
                if role.id in self.bot.muted_roles:
                    role_ids.append(role.id)
        except: pass

        if role_ids is None:
            return

        try: #? Get any muted roles to remove!
            for role_id in role_ids:
                muted_role = utils.DiscordGet(member.guild.roles, id=role_id)
                await member.remove_roles(muted_role, reason='Temp-gag expired.')
        except DiscordException: pass

        try:
            await member.edit(mute=False)
        except DiscordException: pass

        try:
            del self.temporary_mutes[member.id]
        except KeyError: pass

        #! Database Update!
        mod = utils.Moderation.get(member.id)
        mod.gagged = False
        async with self.bot.database() as db:
            await mod.save(db)
            await db('DELETE FROM tempmute_timeout WHERE user_id = $1', member.id)

        log = await utils.ChannelFunction.get_log_channel(guild=member.guild, log="member")
        await log.send(embed=utils.LogEmbed(type="positive", title=f"User Ungagged", desc=f"{member.mention} was ungagged!\n\n**Temp-Gag Has Expired!**"))



    def create_temp_gag_task(self, member:Member, expiration:datetime):
        coro = utils.run_at(expiration, self.handle_mute_expiration, member)
        task = self.bot.loop.create_task(coro)
        self.temporary_mutes[member.id] = (task, expiration)
        return task





    @utils.is_nsfw_staff()
    @command(aliases=['tg'])
    async def tempgag(self, ctx, user:Greedy[Member], duration:utils.TimeConverter, *, reason:str="[No Reason Given]"):
        '''Temporarily applies the prisoner role to a user or users'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)

        for i in user: 
            if any([r for r in i.roles if r.id in self.bot.nsfw_staff]):
                return await ctx.send(embed=utils.WarningEmbed(desc="Staff are unable to be gagged!", guild=ctx.guild))

        try: #! Get the guilds muted role
            for role in ctx.guild.roles:
                if role.id in self.bot.muted_roles:
                    role_id = role.id
        except: return
        if role_id is None: #? Error in Config!
            return await ctx.send("Looks like this guild's muted roles can not be found in my config.", delete_after=15)

        muted_role = utils.DiscordGet(ctx.guild.roles, id=role_id)

        #! Add the role to the user
        for i in user:
            await i.add_roles(muted_role, reason=f'{reason} :: temp gagged by {ctx.author.mention}')
            try: #? Tell them they are gagged!
                await i.send(f'You were temporarily gagged for `{duration}` seconds for reason: `{reason}`.')
            except DiscordException:
                pass

        #! Send message to the channel
        if len(user) == 1:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} gagged {user[0].mention} for {duration} seconds!", guild=ctx.guild))
        else:
            await ctx.send(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} gagged `{len(user)}` users  for {duration} seconds!", guild=ctx.guild))

        #!Save to the DB
        for i in user:
            mod = utils.Moderation.get(i.id)
            mod.gagged = True
            mod.violations += 1
            async with self.bot.database() as db:
                await mod.save(db)
                mute_expiration = datetime.now() + timedelta(seconds=duration)
                await db('INSERT INTO tempmute_timeout VALUES ($1, $2) '
                                'ON CONFLICT (user_id) '
                                'DO UPDATE SET unmute_time = $2', i.id, mute_expiration)
                self.create_temp_gag_task(i, mute_expiration)

        log = await utils.ChannelFunction.get_log_channel(guild=ctx.guild, log="member")
        for i in user:
            await log.send(embed=utils.LogEmbed(type="negative", title=f"User Gagged", desc=f"{i.name} was gagged!\nBy: **{ctx.author}**\nReason :: **{reason}**\nDuration :: **{duration}**"))





def setup(bot):
    x = Muting(bot)
    bot.add_cog(x)