# Discord
from datetime import datetime as dt, timedelta
# Additions
from random import choice
from re import compile

from discord import Message
from discord.ext.commands import Cog
from discord.ext.tasks import loop
from more_itertools import unique_everseen

import utils


class Currency_Gen(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.exp_voice_gen_loop.start()
        self.valid_uri = compile(r"(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")

    @Cog.listener('on_message')
    async def Level_Progression(self, message:Message):
        '''Determine Level progression settings!'''

        # BETTER NOT BE A DM
        if message.guild == None:
            return
        if message.author.bot:
            return
        #? Check if bot is connected!
        if self.bot.connected == False:
            return

        await self.level_progression(message=message)



    async def level_progression(self, message:Message):
        '''Level Progression'''
        lvl = utils.Levels.get(message.author.id)
        if lvl.last_xp == None:
            lvl.last_xp = dt.utcnow()
        if (lvl.last_xp + timedelta(seconds=30)) <= dt.utcnow(): # Check Time

            #! Define varibles
            exp = 1
            unique_words = len(list(unique_everseen(message.content.split(), str.lower)))
            requiredexp = await utils.UserFunction.determine_required_exp(level=lvl.level)
            if message.attachments != None:
                unique_words += 5

            #! Unique Word Nerfer
            if unique_words > 8:
                unique_words = 8
            elif unique_words < 2:
                return

            rng = choice([0.5, 0.75, 1.0, 1.25, 1.50, 2])
            exp += (1+lvl.level/3)*rng
            coins = 1+unique_words*rng

            await utils.CoinFunctions.earn(earner=message.author, amount=coins)

            #! Command Usage Secret Increase!?
            if message.content.startswith(self.bot.config['prefix']):
                exp += lvl.level

            if lvl.exp >= requiredexp:
                await utils.UserFunction.level_up(user=message.author, channel=message.channel)

            #! Save it to database
            lvl.exp += exp+3
            lvl.last_xp = dt.utcnow()
        async with self.bot.database() as db:
            await lvl.save(db)



    def cog_unload(self):
        self.exp_voice_gen.cancel()

    @loop(minutes=5)
    async def exp_voice_gen_loop(self):
        #? Check if bot is connected!
        if self.bot.connected == False:
            return

        coins_payed = 0

        for guild in self.bot.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:

                    tr = utils.Tracking.get(member.id)
                    tr.vc_mins += 5
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
                        break
                    if len(vc.members) < 2:
                        break

                    c = utils.Currency.get(member.id)
                    lvl = utils.Levels.get(member.id)
                    lvl.exp += 15+(len(vc.members)/2)*(lvl.level/3)
                    coins = 5 + round(len(vc.members))
                    await utils.CoinFunctions.earn(earner=member, amount=coins)

                    requiredexp = await utils.UserFunction.determine_required_exp(level=lvl.level)
                    if lvl.exp >= requiredexp:
                        await utils.UserFunction.level_up(user=member, channel=None)

                    async with self.bot.database() as db:
                        await c.save(db)
                        await lvl.save(db)




    @exp_voice_gen_loop.before_loop
    async def before_exp_voice_gen_loop(self):
        await self.bot.wait_until_ready()



def setup(bot):
    x = Currency_Gen(bot)
    bot.add_cog(x)
