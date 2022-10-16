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
from re import compile

import utils

class Currency_Gen(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.exp_voice_gen_loop.start()
        self.valid_uri = compile(r"(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")

    @Cog.listener('on_message')
    async def on_message(self, message:Message):
        '''Determine Level progression settings!'''

        #? BETTER NOT BE A DM
        if message.guild == None:
            return
        if message.author.bot:
            return
        #? Check if bot is connected!
        if self.bot.connected == False:
            return

        tr = utils.Tracking.get(message.author.id)
        tr.messages += 1
        async with self.bot.database() as db:
                await tr.save(db)


        #? Check for links
        if message.attachments != None: 
            await self.coin_gen(message=message, image=True)
        elif message.content.strip().lower() != self.valid_uri.match(message.content.split(" ")[0].split("\n")[0]):
            await self.coin_gen(message=message)
        else:
            await self.coin_gen(message=message, image=True)




    async def coin_gen(self, message:Message, image:bool=False):
        '''Level Progression'''
        c = utils.Currency.get(message.author.id)
        if c.last_coin == None:
            c.last_coin = dt.utcnow()
        if (c.last_coin + timedelta(seconds=30)) <= dt.utcnow(): # Check Time

            #! Define varibles
            unique_words = len(list(unique_everseen(message.content.split(), str.lower)))

            #! Unique Word Checker
            if unique_words > 3:
                c.coins += 5
            elif image == True:
                c.coins += 3
            c.last_coin = dt.utcnow()

            async with self.bot.database() as db:
                await c.save(db)






    def cog_unload(self):
        self.exp_voice_gen.cancel()

    @loop(minutes=10)
    async def exp_voice_gen_loop(self):
        #? Check if bot is connected!
        if self.bot.connected == False:
            return

        for guild in self.bot.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:

                    tr = utils.Tracking.get(member.id)
                    tr.vc_mins += 1
                    async with self.bot.database() as db:
                        await tr.save(db)

                    #! Checks
                    checks = [
                        member.voice.deaf, 
                        member.voice.mute, 
                        member.voice.self_mute, 
                        member.voice.self_deaf, 
                        member.voice.afk,
                        member.bot,
                    ]
                    if any(checks):
                        return
                    if len(vc.members) < 2:
                        return

                    c = utils.Currency.get(member.id)
                    coins = 4 + round(len(vc.members)/2)
                    c.coin += coins

                    async with self.bot.database() as db:
                        await c.save(db)



    @exp_voice_gen_loop.before_loop
    async def before_exp_voice_gen_loop(self):
        await self.bot.wait_until_ready()



def setup(bot):
    x = Currency_Gen(bot)
    bot.add_cog(x)
