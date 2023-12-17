# Discord
from datetime import datetime as dt, timedelta
from random import choice

import discord
from discord.ext.commands import command, Cog, ApplicationCommandMeta, cooldown, BucketType

import utils


class Pinging(Cog):
    def __init__(self, bot):
        self.bot = bot


    @cooldown(1, 3600, BucketType.channel)
    @command(        
        aliases=['mention'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="role",
                    description="The role you would like to ping.",
                    type=ApplicationCommandOptionType.role,
                    required=True,
                ),
            ],
        ),
    )
    async def ping(self, ctx, role):
        """Ping a ping role!"""

        if role.id == 1134359929625526353:
            await ctx.interaction.response.send_message(content="<@&1134359929625526353>", embed=utils.DefaultEmbed(title=f"You have all been summoned to SCP!"))
            return

        if role.id == 1134574072051806308:
            await ctx.interaction.response.send_message(content="<@&1134574072051806308>", embed=utils.DefaultEmbed(title=f"You have all been summoned to join a VC!"))
            return

        if role.id == 1185903654100795413:
            await ctx.interaction.response.send_message(content="<@&1185903654100795413>", embed=utils.DefaultEmbed(title=f"You have all been summoned to join the Minecraft Server!"))
            return

        await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(title=f"That's not a pingable role!"))
        return




def setup(bot):
    x = Pinging(bot)
    bot.add_cog(x)
