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
        self.exp_voice_gen_loop.start()
        self.restart = True


    @property  #! The currency logs
    def currency_log(self):
        return self.bot.get_channel(self.bot.config['channels']['currency_log']) #?Currency log channel


    @Cog.listener('on_message')
    async def Level_Progression(self, message:Message):
        '''Determine Level progression settings!'''

        #! BETTER NOT BE A DM
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
        track = utils.Tracking.get(message.author.id)
        track.messages += 1
        if lvl.last_xp == None:
            lvl.last_xp = dt.utcnow()
        if (lvl.last_xp + timedelta(seconds=30)) <= dt.utcnow(): # Check Time

            #! Define varibles
            exp = 2
            unique_words = len(list(unique_everseen(message.content.split(), str.lower)))
            requiredexp = await utils.UserFunction.determine_required_exp(level=lvl.level)

            #! Unique Word Nerfer
            if unique_words > 15:
                unique_words = 15

            rng = choice([0.75, 1.0, 1.25, 1.50, 2.0])
            exp += (lvl.level/6) + (unique_words*rng)
            reward = (unique_words/8)*rng
            c.gold_coins += reward 

            #! Command Usage Secret Increase!?
            if message.content.startswith(self.bot.config['prefix']):
                exp += lvl.level

            #! Level Up
            if lvl.exp >= requiredexp:
                await utils.UserFunction.level_up(user=message.author, channel=message.channel)

            #! Save it to database
            lvl.exp += exp
            lvl.last_xp = dt.utcnow()
        async with self.bot.database() as db:
            await lvl.save(db)
            await track.save(db)
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
                        continue
                    if len(vc.members) < 2:
                        continue

                    #? Update their user
                    lvl = utils.Levels.get(member.id)
                    c = utils.Currency.get(member.id)
                    track = utils.Tracking.get(member.id)
                    ss = utils.Settings.get(member.id)
                    exp = 10 + (len(vc.members)*2.75) + (lvl.level/3)
                    gold = 5 + round(len(vc.members)*5.25)
                    lvl.exp += round(exp)
                    c.gold_coins += gold
                    track.vc_mins += 10

                    requiredexp = await utils.UserFunction.determine_required_exp(level=lvl.level)
                    if lvl.exp >= requiredexp:
                        await utils.UserFunction.level_up(user=member, channel=None)

                    async with self.bot.database() as db:
                        await lvl.save(db)
                        await c.save(db)
                        await track.save(db)


                    if ss.vc_msgs == True:
                        await member.send(embed=utils.LogEmbed(type="positive", title=f"VC Earnings!", desc=f"{member.mention} earned **{round(exp):,} EXP!**\n**{gold:,} {self.bot.config['emotes']['goldcoin']} From being in VC!**"))

                    await self.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"VC Earnings!", desc=f"{member.mention} earned **{round(exp):,} EXP!**\n**{gold:,} {self.bot.config['emotes']['goldcoin']} From being in VC!**"))


    @exp_voice_gen_loop.before_loop
    async def before_exp_voice_gen_loop(self):
        await self.bot.wait_until_ready()



def setup(bot):
    x = Listeners(bot)
    bot.add_cog(x)
