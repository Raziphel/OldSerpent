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

    @property  # ! The message logs
    def message_log(self):
        return self.bot.get_channel(self.bot.config['channels']['messages'])

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
    async def prune(self, ctx, user:User, amount: int = 10):
        """Purges the given amount of messages from the channel."""
        check = lambda m: m.author.id == user.id

        # ! Add max amount
        if amount > 250:
            return await ctx.interaction.response.send_message(f"**250 is the maximum amount of messages.**")

        # ! Report and log the purging!
        st = utils.Staff_Track.get(ctx.author.id)
        st.purges += 1
        async with self.bot.database() as db:
            await st.save(db)
        removed = await ctx.channel.purge(limit=amount, check=check)
        await ctx.interaction.response.send_message(
            embed=utils.SpecialEmbed(
                title=f"Deleted {len(removed)} messages!",
                guild=ctx.guild
            )
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
    async def purge(self, ctx, amount: int = 10):
        """Purges the given amount of messages from the channel."""
        check = lambda m: True

        # ! Add max amount
        if amount > 250:
            return await ctx.interaction.response.send_message(f"**250 is the maximum amount of messages.**")

        # ! Report and log the purging!
        st = utils.Staff_Track.get(ctx.author.id)
        st.purges += 1
        async with self.bot.database() as db:
            await st.save(db)
        removed = await ctx.channel.purge(limit=amount, check=check)
        await ctx.interaction.response.send_message(
            embed=utils.SpecialEmbed(
                title=f"Deleted {len(removed)} messages!",
                guild=ctx.guild
            )
        )



        await self.message_log.send(
            embed=utils.LogEmbed(
                type="negative",
                title=f"Channel messages Purged",
                desc=f"<@{ctx.author.id}> purged {amount} messages from <#{ctx.channel.id}>!"
            )
        )

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
