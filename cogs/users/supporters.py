# Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter
from discord import Member, Message, User, Game, Embed
from discord import Member, Message, User, TextChannel, Role, RawReactionActionEvent, Embed
# Additions
from datetime import datetime as dt, timedelta
from asyncio import iscoroutine, gather, sleep
from math import floor 
from random import choice, randint

import utils


class supporters(Cog):

    def __init__(self, bot):
        self.bot = bot


    @command(aliases=['Monthly', 'claim', "Claim"])
    async def monthly(self, ctx):
        '''Supporters monthly claim of rewards!'''









def setup(bot):
    x = supporters(bot)
    bot.add_cog(x)