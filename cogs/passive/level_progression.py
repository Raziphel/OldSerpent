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

class Level_Progression(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.exp_voice_gen_loop.start()

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
        c = utils.Currency.get(message.author.id)
        if lvl.last_xp == None:
            lvl.last_xp = dt.utcnow()
        if (lvl.last_xp + timedelta(seconds=30)) <= dt.utcnow(): # Check Time

            #! Define varibles
            exp = 1
            unique_words = len(list(unique_everseen(message.content.split(), str.lower)))
            requiredexp = await utils.UserFunction.determine_required_exp(level=lvl.level)

            #! Unique Word Nerfer
            if unique_words > 10:
                unique_words = 10

            rng = choice([0.5, 0.75, 1.0, 1.25, 1.50])
            exp += lvl.level*rng
            c.silver += unique_words*rng

            #! Command Usage Secret Increase!?
            if message.content.startswith(self.bot.config['prefix']):
                exp += lvl.level

            if lvl.exp >= requiredexp:
                await utils.UserFunction.level_up(user=message.author, channel=message.channel)

            #! Check for needed update?
            if c.silver >= 100:
                await utils.GemFunction.update_gems(user=message.author)

            #! Save it to database
            lvl.exp += exp
            lvl.last_xp = dt.utcnow()
        async with self.bot.database() as db:
            await lvl.save(db)



    def cog_unload(self):
        self.exp_voice_gen.cancel()

    @loop(minutes=15)
    async def exp_voice_gen_loop(self):
        #? Check if bot is connected!
        if self.bot.connected == False:
            return

        for guild in self.bot.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:

                    # Checks
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

                    # Update their user
                    ss = utils.Settings.get(member.id)
                    lvl = utils.Levels.get(member.id)
                    c = utils.Currency.get(member.id)
                    exp = len(vc.members)*(lvl.level/2)
                    silver = 5 + round(len(vc.members)/2)
                    lvl.exp += exp
                    c.silver += silver

                    requiredexp = await utils.UserFunction.determine_required_exp(level=lvl.level)
                    if lvl.exp >= requiredexp:
                        await utils.UserFunction.level_up(user=member, channel=None)

                    async with self.bot.database() as db:
                        await lvl.save(db)
                        await c.save(db)

                    if ss.vc_msgs == True:
                        await member.send(embed=utils.SpecialEmbed(title=f"VC Earnings!", desc=f"You earned **{exp:,} EXP!**\nAnd **{coins:,} Coins!**"))

    @exp_voice_gen_loop.before_loop
    async def before_exp_voice_gen_loop(self):
        await self.bot.wait_until_ready()



def setup(bot):
    x = Level_Progression(bot)
    bot.add_cog(x)
