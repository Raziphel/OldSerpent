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


    @Cog.listener('on_message')
    async def vote_channels(self, message):
        '''
        Adds votes reactions!
        '''

        # Check for general
        if message.channel.id != 1047024954614480957: #? Scp suggestions
            return
        else:
            await message.add_reaction("<:UpVote:1041606985080119377>")
            await message.add_reaction("<:DownVote:1041606970492342282>")




def setup(bot):
    x = Listeners(bot)
    bot.add_cog(x)
