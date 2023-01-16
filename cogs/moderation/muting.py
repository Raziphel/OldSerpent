
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

    @property  #! The members logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['channels']['server']) 


    @Cog.listener()
    async def on_member_join(self, member):
        '''Catches jail breakers~!'''

        guild = member.guild

        mod = utils.Moderation.get(member.id)
        if mod.muted == True: #! Checks to make sure they were muted!
            try: #! Get the guilds muted role
                for role in ctx.guild.roles:
                    if role.id == 1028881308006502400:
                        role_id = role.id
                muted_role = utils.DiscordGet(ctx.guild.roles, id=role_id)
                await member.add_roles(muted_role)
            except: return

            await self.discord_log.send(embed=utils.LogEmbed(type="negative", title=f"Prisoner Tried to escape...", desc=f"{member} Was thrown back into the dungeons."))






    @utils.is_admin_staff()
    @command()
    async def ban(self, ctx, user:Greedy[Member], *, reason:Optional[str]="[No Reason Given]"):
        '''Bans any given amount of members given!'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)

        for i in user: 
            if any([r for r in i.roles if r.id == 891793700932431942]):
                return await ctx.send(embed=utils.WarningEmbed(desc="Staff can't be banned!  Please demote first!", guild=ctx.guild))

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
        for i in user:
            await self.discord_log.send(embed=utils.LogEmbed(type="negative", author=f"User Banned", desc=f"{i.name} was banned!\n**By: {ctx.author}\nReason :: {reason}**"))




    @utils.is_mod_staff()
    @command(aliases=['g', 'gag'])
    async def mute(self, ctx, user:Greedy[Member], *, reason:Optional[str]="[No Reason Given]"):
        '''Applies the prisoner role to a user or users'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)

        for i in user: 
            if any([r for r in i.roles if r.id in self.bot.nsfw_staff]):
                return await ctx.send(embed=utils.WarningEmbed(desc="Staff are unable to be muted!", guild=ctx.guild))

        try: #! Get the guilds muted role
            for role in ctx.guild.roles:
                if role.id == 1028881308006502400:
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
            await i.add_roles(muted_role, reason=f'{reason} :: muted by {ctx.author.mention}')
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
            mod.violations += 1
        async with self.bot.database() as db:
            await mod.save(db)

        for i in user:
            await self.discord_log.send(embed=utils.LogEmbed(type="negative", title=f"User Gagged", desc=f"{i.name} was muted!\nBy: **{ctx.author}**\nReason :: **{reason}**"))




    @utils.is_mod_staff()
    @command(aliases=['ungag'])
    async def unmute(self, ctx, user:Greedy[Member], *, reason:Optional[str]="[No Reason Given]"):
        '''Removes the prisoner role to a user or users'''

        if len(user) == 0:
            return await ctx.send('Please specify a valid user.', delete_after=15)


        #! Remove the roles from the users
        role_ids = []
        try: #! Get the guilds muted role
            for role in member.guild.roles:
                if role.id == 1028881308006502400:
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
            await self.discord_log.send(embed=utils.LogEmbed(type="negative", title=f"User Un-Gagged", desc=f"{i.name} was un-muted!\nBy: **{ctx.author}**\nReason :: **{reason}**"))







def setup(bot):
    x = Muting(bot)
    bot.add_cog(x)