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

class Miners(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mine_loops.start()
        self.virgin = True


    @property  #! The currency logs
    def currency_log(self):
        return self.bot.get_channel(self.bot.config['channels']['currency_log']) #?Currency log channel




    def cog_unload(self):
        self.exp_voice_gen.cancel()

    @loop(minutes=480)
    async def mine_loops(self):
        #? Check if bot is connected!
        if self.bot.connected == False:
            return

        #* Setup the emoji names
        emerald = self.bot.config['emotes']['emerald']
        diamond = self.bot.config['emotes']['diamond']
        ruby = self.bot.config['emotes']['ruby']
        sapphire = self.bot.config['emotes']['sapphire']
        amethyst = self.bot.config['emotes']['amethyst']
        crimson = self.bot.config['emotes']['crimson']

        if self.virgin == True:
            self.virgin = False
            return

        e = 0
        d = 0
        r = 0
        s = 0
        a = 0
        cr = 0

        for guild in self.bot.guilds:
                for member in guild.members:
                    #? Update their user
                    m = utils.Miners.get(member.id)
                    c = utils.Currency.get(member.id)


                    if m.emerald > 0:
                        e += (m.emerald*2)
                        c.emerald += e
                    if m.diamond > 0:
                        d += (m.diamond*0.5)
                        c.diamond += d
                    if m.ruby > 0:
                        r += (m.ruby*0.25)
                        c.ruby += r
                    if m.sapphire > 0:
                        s += (m.sapphire*0.1)
                        c.sapphire += s
                    if m.amethyst > 0:
                        a += (m.amethyst*0.05)
                        c.amethyst += a
                    if m.crimson > 0:
                        cr += (m.crimson*0.01)
                        c.crimson += cr

                    async with self.bot.database() as db:
                        await c.save(db)


        await self.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"Miner Earnings!", desc=f"❧ {emerald} : **{e}**\n❧ {diamond} : **{d}**\n❧ {ruby} : **{r}**\n❧ {sapphire} : **{s}**\n❧ {amethyst} : **{a}**\n❧ {crimson} : **{cr}**"))


    @mine_loops.before_loop
    async def before_mine_loops(self):
        await self.bot.wait_until_ready()



def setup(bot):
    x = Miners(bot)
    bot.add_cog(x)
