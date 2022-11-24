# Discord
from discord.ext.commands import command, Cog
from discord import Member, Message, User, TextChannel
from discord.ext.tasks import loop
# Additions
from random import randint, choice
from datetime import datetime as dt, timedelta
from more_itertools import unique_everseen
from re import search
from asyncio import sleep

import utils

class Listeners(Cog):
    def __init__(self, bot):
        self.bot = bot





def setup(bot):
    x = Listeners(bot)
    bot.add_cog(x)
