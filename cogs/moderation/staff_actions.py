# * Discord
from discord import ApplicationCommandOption, ApplicationCommandOptionType
from discord import Member, User, Embed
from discord.ext.commands import ApplicationCommandMeta
from discord.ext.commands import command, Cog

# * Additions
import utils
from typing import Optional


class Staff_Actions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #! The members logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['channels']['logs']['discord']) 

    @property  #! The message logs
    def message_log(self):
        return self.bot.get_channel(self.bot.config['channels']['logs']['messages']) 





    @utils.is_admin_staff()
    @command(
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user to be banned from the server!",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
                ApplicationCommandOption(
                    name="reason",
                    description="The reason for being banned!",
                    type=ApplicationCommandOptionType.string,
                    required=True,
                ),
            ],
        ),
    )
    async def ban(self, ctx, user:Member, *, reason:Optional[str]="[No Reason Given]"):
        '''Bans any given amount of members given!'''

        if not user:
            return await ctx.interaction.response.send_message('Please specify a valid user.', delete_after=15)

        #+ Ban that loser!
        if user:
            #! Ban hammer message
            try:
                await user.send(F"**Sorry, you were banned from {ctx.guild} for: {reason}**\n\n**Honestly man thats a rip...\nI doubt you will be missed tho! c:**")
            except: pass
            await ctx.guild.ban(user, delete_message_days=0, reason=f'{reason} :: banned by {ctx.author!s}')

        #! Report who has been banned!
        await ctx.interaction.response.send_message(embed=utils.WarningEmbed(title=f"Banned `{user}`."))
        await self.server_logs.send(embed=utils.LogEmbed(type="negative", title=f"User Banned", desc=f"{user.name} was banned!\n**By: {ctx.author}\nReason :: {reason}**"))







    @utils.is_mod_staff()
    @command(application_command_meta=ApplicationCommandMeta(), aliases=['iban'])
    async def imageban(self, ctx, user:Member):
        '''Restarts the bot'''  
        mod = utils.Moderation.get(user.id)
        mod.image_banned = True
        async with self.bot.database() as db:
            await mod.save(db)

        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild

        image_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['image_pass'])
        await user.remove_roles(image_pass, reason="Removed Image Pass role.")
        await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(title=f"{user} is now image pass banned!"))
        await self.discord_log.send(embed=utils.LogEmbed(type="negative", title=f"{user.name} has been image banned.", thumbnail=member.avatar.url))







    @utils.is_mod_staff()
    @command(
        aliases=['pr'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="User whose messages you want to delete.",
                    type=ApplicationCommandOptionType.user,
                    required=False,
                ),
                ApplicationCommandOption(
                    name="amount",
                    description="Amount of messages you want to delete.",
                    type=ApplicationCommandOptionType.integer,
                    required=False,
                ),
            ],
        )
    )
    async def prune(self, ctx, user:User, amount: int = 100):
        """Purges message from a specific user!"""
        check = lambda m: m.author.id == user.id

        # ! Add max amount
        if amount > 250:
            return await ctx.interaction.response.send_message(f"**250 is the maximum amount of messages.**")

        # ! Report and log the purging!
        removed = await ctx.channel.purge(limit=amount, check=check)
        await ctx.interaction.response.send_message(embed=utils.SpecialEmbed(title=f"Deleted {len(removed)} messages!")
        )


    @utils.is_mod_staff()
    @command(
        aliases=['pu'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="amount",
                    description="Amount of messages you want to delete.",
                    type=ApplicationCommandOptionType.integer,
                    required=False,
                ),
            ],
        )
    )
    async def purge(self, ctx, amount: int = 100):
        """Purges the given amount of messages from the channel."""
        check = lambda m: True

        # ! Add max amount
        if amount > 250:
            return await ctx.interaction.response.send_message(f"**250 is the maximum amount of messages.**")

        # ! Report and log the purging!
        removed = await ctx.channel.purge(limit=amount, check=check)
        await ctx.interaction.response.send_message(
            embed=utils.SpecialEmbed(
                title=f"Deleted {len(removed)} messages!",
                guild=ctx.guild
            )
        )
        await self.message_log.send(embed=utils.LogEmbed(type="negative", title=f"Channel messages Purged",desc=f"<@{ctx.author.id}> purged {amount} messages from <#{ctx.channel.id}>!"))

    @utils.is_mod_staff()
    @command(
        aliases=['cl'],
        application_command_meta=ApplicationCommandMeta(),
    )
    async def clean(self, ctx):
        """Clears the bot's messages!"""
        check = lambda m: m.author.id == self.bot.user.id or m.id == ctx.message.id or m.content.startswith(
            self.bot.config['prefix'])
        await ctx.channel.purge(check=check)

    @utils.is_mod_staff()
    @command(
        aliases=['whos'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="User you want more information about.",
                    type=ApplicationCommandOptionType.user,
                    required=False,
                ),
            ],
        )
    )
    async def whois(self, ctx, user: Member = None):
        """Gives information on the user!"""
        if not user:
            user = ctx.author
        embed = Embed(title=f"{user}'s Member Information", description=f"", color=0x1d89e3)
        created_at = user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        joined_at = user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        embed.add_field(name="Joined", value=f'{joined_at}', inline=True)
        embed.add_field(name="Registered", value=f'{created_at}', inline=True)
        roles = []
        for i in user.roles:
            roles.append(f"{i.mention}")
        role_string = ', '.join(roles)
        embed.add_field(name=f"Roles [{len(user.roles)}]", value=f'{role_string}', inline=False)
        perm_list = [perm[0] for perm in user.guild_permissions if perm[1]]
        perm_string = ', '.join(perm_list)
        embed.add_field(name=f"Perm-Level", value=f'{perm_string}', inline=True)
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    x = Staff_Actions(bot)
    bot.add_cog(x)
