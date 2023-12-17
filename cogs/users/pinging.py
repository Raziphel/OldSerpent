from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter, ApplicationCommandMeta
from discord import Member, Message, User, Game, Embed, TextChannel, Role, RawReactionActionEvent, ApplicationCommandOption, ApplicationCommandOptionType

#* Additions
from datetime import datetime as dt, timedelta
from asyncio import iscoroutine, gather, sleep
from math import floor 
from random import choice, randint

import utils



class Pinging(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scpping = dt(year=2000, month=1, day=1)
        self.mcping = dt(year=2000, month=1, day=1)
        self.lethalping = dt(year=2000, month=1, day=1)
        self.vcping = dt(year=2000, month=1, day=1)


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
    async def sendping(self, ctx, role):
        """Ping a ping role!"""

        
        if role == "1134359929625526353":
            if (self.scpping + timedelta(hours=2)) >= dt.utcnow():
                await ctx.interaction.response.send_message(content="<@&1134359929625526353>", embed=utils.DefaultEmbed(title=f"You have all been summoned to SCP!"))
                self.scpping = dt.utcnow()
            else:
                await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(title=f"You are pinging again too soon!"))
            return

        if role == "1134574072051806308":
            if (self.scpping + timedelta(hours=2)) >= dt.utcnow():
                await ctx.interaction.response.send_message(content="<@&1134574072051806308>", embed=utils.DefaultEmbed(title=f"You have all been summoned to join a VC!"))
                self.vcping = dt.utcnow()
            else:
                await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(title=f"You are pinging again too soon!"))
            return

        if role == "1185903654100795413":
            if (self.scpping + timedelta(hours=2)) >= dt.utcnow():
                await ctx.interaction.response.send_message(content="<@&1185903654100795413>", embed=utils.DefaultEmbed(title=f"You have all been summoned to join the Minecraft Server!"))
                self.mcping = dt.utcnow()
            else:
                await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(title=f"You are pinging again too soon!"))
            return

        if role == "1185903816407785502":
            if (self.scpping + timedelta(hours=2)) >= dt.utcnow():
                await ctx.interaction.response.send_message(content="<@&1185903816407785502>", embed=utils.DefaultEmbed(title=f"You have all been summoned to play on the Lethal Modpack!"))
                self.lethalping = dt.utcnow()
            else:
                await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(title=f"You are pinging again too soon!"))
            return


        await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(title=f"That's not a pingable role!"))
        return




def setup(bot):
    x = Pinging(bot)
    bot.add_cog(x)
