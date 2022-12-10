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

        tr = utils.Tracking.get(message.author.id)
        tr.messages += 1
        async with self.bot.database() as db:
            await tr.save(db)

        # Check for general
        if message.channel.id in [1047026469068623902, 1047024954614480957]: #? Suggestions
            await message.add_reaction("<:UpVote:1041606985080119377>")
            await message.add_reaction("<:DownVote:1041606970492342282>")
        if message.channel.id in [1051033412456165396]: #? 1 word only
            total_words = len(message.content.split())
            if total_words > 1 or list(message.content) in ["=", "-", "_", "~", "`", "."]:
                await message.delete()
                await message.channel.send(embed=utils.DefualtEmbed(title="1 Word Only!", desc="If it wasn't obvious you can only send 1 word."), delete_after=5)




def setup(bot):
    x = Listeners(bot)
    bot.add_cog(x)
