from datetime import datetime as dt, timedelta
from random import choice

from discord.ext.commands import Cog
from discord.ext import tasks
from discord import Member, Message, User, Game, Embed, Color

import math
from random import randint, choice

import utils


class Startup(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botpres_loop.start()


    @tasks.loop(minutes=2)
    async def botpres_loop(self):
        '''updates the bot's presence!'''
        playing = "Being Created!"
        await self.bot.change_presence(activity=Game(name=playing)) 


    @botpres_loop.before_loop
    async def bot_pres_update(self):
        '''Waits until the cache loads up before running the pres loop'''
        await self.bot.wait_until_ready()


def setup(bot):
    x = Startup(bot)
    bot.add_cog(x)
