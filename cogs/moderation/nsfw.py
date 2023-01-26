# * Discord
from discord import Member, ApplicationCommandOption, ApplicationCommandOptionType
from discord.ext.commands import command, Cog, ApplicationCommandMeta

import utils


class Nsfw(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  # ! The members logs
    def members_log(self):
        return self.bot.get_channel(self.bot.config['members_log'])

    @utils.is_mod_staff()
    @utils.is_guild()
    @command(
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user you want to remove NSFW access from.",
                    type=ApplicationCommandOptionType.user,
                    required=False,
                ),
            ],
        )
    )
    async def child(self, ctx, user: Member):
        """Removes nsfw access from a user!"""
        await self.notnsfw_user(guild=ctx.guild, user=user)
        st = utils.Staff_Track.get(ctx.author.id)
        st.purges += 1

        async with self.bot.database() as db:
            await st.save(db)

        await ctx.send(
            embed=utils.WarningEmbed(
                title=f"{user.mention}, has been marked as a child!",
                guild=ctx.guild
            )
        )

    async def notnsfw_user(self, guild, user: Member):
        role = utils.DiscordGet(guild.roles, name="Adult 🚬")
        mod = utils.Moderation.get(user.id)
        try:  # ! Removes 18+ role if exists!
            await user.remove_roles(role)
        except:
            pass
        role = utils.DiscordGet(user.guild.roles, name="Child 🍼")
        await user.add_roles(role)
        mod.nsfw = True
        async with self.bot.database() as db:
            await mod.save(db)
        # ! Log the action!
        await self.members_log.send(
            embed=utils.LogEmbed(type="negative", title=f"CHILD ROLE", desc=f"{user.name} was marked as a child!",
                                 guild=guild))

    @utils.is_mod_staff()
    @utils.is_guild()
    @command(
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user you want to grant NSFW access to.",
                    type=ApplicationCommandOptionType.user,
                    required=False,
                ),
            ],
        )
    )
    async def adult(self, ctx, user: Member):
        """Add Adult access from a user!"""
        await self.nsfw_user(user=user, guild=ctx.guild)
        st = utils.Staff_Track.get(ctx.author.id)
        st.purges += 1

        async with self.bot.database() as db:
            await st.save(db)

        await ctx.send(
            embed=utils.WarningEmbed(
                title=f"{user.mention}, has been marked as Adult!\nHappy Birthday, probably.",
                guild=ctx.guild
            )
        )

    async def nsfw_user(self, user: Member, guild):
        role = utils.DiscordGet(guild.roles, name="Child 🍼")
        await user.remove_roles(role)

        mod = utils.Moderation.get(user.id)
        mod.nsfw = False

        async with self.bot.database() as db:
            await mod.save(db)

        # ! Report and log the action!
        await self.members_log.send(
            embed=utils.LogEmbed(
                type="positive",
                title=f"ADULT ROLE",
                desc=f"{user.name} has been marked as an adult."
            )
        )


def setup(bot):
    x = Nsfw(bot)
    bot.add_cog(x)
