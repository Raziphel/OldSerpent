
#* Discord
from discord.ext.commands import command, Cog, Greedy, ApplicationCommandMeta
from discord import Member, DiscordException
from discord import ApplicationCommandOption, ApplicationCommandOptionType

# * Additions
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
    @command(
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user to be permenantly muted & messages purged of!",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
                ApplicationCommandOption(
                    name="reason",
                    description="The reason for being muted",
                    type=ApplicationCommandOptionType.string,
                    required=False,
                ),
            ],
        ),
    )
    async def mute(self, ctx, user:Member, *, reason:Optional[str]="[No Reason Given]"):
        '''Applies the prisoner role to a user or users'''

        if not user:
            return await ctx.interaction.response.send_message('Please specify a valid user.', delete_after=15)


        #? check if it's a purge gag!
        try:
            await ctx.channel.purge(limit=100, check=lambda message: message.author.id == user.id)
        except: pass


        muted_role = utils.DiscordGet(ctx.guild.roles, id=1028881308006502400)

        #! Add the role to the user
        if user:
            await user.add_roles(muted_role, reason=f'{reason} :: muted by {ctx.author.mention}')
            try:
                await user.edit(mute=True)
            except DiscordException: pass
            try: #? Tell them they are muted!
                await user.send(f'You were permanently muted for reason `{reason}`')
            except DiscordException:
                pass
            await ctx.interaction.response.send_message(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} muted {user[0].mention} permenantly!", guild=ctx.guild))

        #!Save to the DB
        mod = utils.Moderation.get(i.id)
        mod.muted = True
        async with self.bot.database() as db:
            await mod.save(db)

        await self.server_logs.send(embed=utils.LogEmbed(type="negative", title=f"User Muted", desc=f"{i.name} was muted!\nBy: **{ctx.author}**\nReason :: **{reason}**"))




    @utils.is_mod_staff()
    @command(
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user to be un-muted!",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
                ApplicationCommandOption(
                    name="reason",
                    description="The reason for being un-muted",
                    type=ApplicationCommandOptionType.string,
                    required=False,
                ),
            ],
        ),
    )
    async def unmute(self, ctx, user:Member, *, reason:Optional[str]="[No Reason Given]"):
        '''Removes the prisoner role to a user or users'''

        if not user:
            return await ctx.interaction.response.send_message('Please specify a valid user.', delete_after=15)


        #+ Unmute that loser!
        if user:
            muted_role = utils.DiscordGet(ctx.guild.roles, id=1028881308006502400)
            await user.remove_roles(muted_role, reason='Mute removed.')
            await user.remove_roles(muted_role, reason=f'{reason} :: muted removed by {ctx.author.mention}')
            await ctx.interaction.response.send_message(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} un-muted {user.mention}!", guild=ctx.guild))
            try:
                    await user.edit(mute=True)
            except DiscordException: pass

        #!Save to the DB
        mod = utils.Moderation.get(user.id)
        mod.muted = False
        async with self.bot.database() as db:
            await mod.save(db)

        await self.server_logs.send(embed=utils.LogEmbed(type="negative", title=f"User Un-Muted", desc=f"{user.name} was un-muted!\nBy: **{ctx.author}**\nReason :: **{reason}**"))






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





    @utils.is_mod_staff()
    @command(
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user to be temporarily muted!",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
                ApplicationCommandOption(
                    name="duration",
                    description="How long they should be muted: 1m; 1h or 1d",
                    type=ApplicationCommandOptionType.string,
                    required=True,
                ),
                ApplicationCommandOption(
                    name="reason",
                    description="The reason for being muted",
                    type=ApplicationCommandOptionType.string,
                    required=False,
                ),
            ],
        ),
    )
    async def tempmute(self, ctx, user:Member, duration:utils.TimeConverter, *, reason:str="[No Reason Given]"):
        '''Temporarily applies the prisoner role to a user or users'''

        if not user:
            return await ctx.interaction.response.send_message('Please specify a valid user.')

        #+ Mute that loser
        if user:
            muted_role = utils.DiscordGet(ctx.guild.roles, id=1028881308006502400)
            await user.add_roles(muted_role, reason=f'{reason} :: temp muted by {ctx.author.mention}')
            try: #? Tell them they are muted!
                await user.send(f'You were temporarily muted for `{duration}` seconds for: `{reason}`.')
            except DiscordException:
                pass

        #! Send message to the channel!
        await ctx.interaction.response.send_message(embed=utils.WarningEmbed(desc=f"{ctx.author.mention} muted {user.mention} for {duration} seconds!"))

        #!Save to the DB
        mod = utils.Moderation.get(user.id)
        mod.gagged = True
        async with self.bot.database() as db:
            await mod.save(db)
            mute_expiration = datetime.now() + timedelta(seconds=duration)
            await db('INSERT INTO tempmute_timeout VALUES ($1, $2) '
                            'ON CONFLICT (user_id) '
                            'DO UPDATE SET unmute_time = $2', user.id, mute_expiration)
            self.create_temp_gag_task(user, mute_expiration)

            await self.server_logs.send(embed=utils.LogEmbed(type="negative", title=f"User Muted", desc=f"{user.name} was gagged!\nBy: **{ctx.author}**\nReason :: **{reason}**\nDuration :: **{duration}**"))










def setup(bot):
    x = Muting(bot)
    bot.add_cog(x)