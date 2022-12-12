# Discord
from discord.ext.commands import command, cooldown, BucketType, Cog
from discord import Member, Message, User

from datetime import datetime as dt, timedelta
from math import floor
from random import choice

import utils

class Daily(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command()
    async def daily(self, ctx):
        '''Claim you daily rewards!'''

        #! Define Varibles
        day = utils.Daily.get(ctx.author.id)
        lvl = utils.Levels.get(ctx.author.id)
        c = utils.Currency.get(ctx.author.id)
        if day.premium == False:
            footer = " ~ Hasn't unlocked Bonus Rewards ~"
        else:
            footer = "Click a reward!"

        #! Check if it's first daily
        if day.daily == None:
            day.daily = 1
            day.last_daily = (day.last_daily - timedelta(days=5))
        #! Check if already claimed
        if (day.last_daily + timedelta(hours=24)) >= dt.utcnow():
            tf = day.last_daily + timedelta(hours=20)
            t = dt(1,1,1) + (tf - dt.utcnow())
            await ctx.send(embed=utils.SpecialEmbed(desc=f"You can claim your daily rewards in {t.hour} hours and {t.minute} minutes!"))
            return
        #! Missed daily
        elif (day.last_daily + timedelta(days=3)) <= dt.utcnow():
            day.daily = 1
        #! Got daily
        elif (day.last_daily + timedelta(hours=20)) <= dt.utcnow():
            day.daily += 1

        rng = choice([1, 1.25, 1.5, 1.75, 2, 3])

        #! Determine reward varibles
        if day.daily >= 365:
            daily = 365
        else: daily = day.daily
        coins = round((100+daily)*rng)
        coins = await utils.CoinFunctions.pay_tax(payer=ctx.author, amount=coins)
        c.coins += coins

        #! Add xP!
        xp = round((lvl.level*2.25)*rng)
        lvl.exp += xp

        emoji = choice(['💫', '💙', '♻', '⚜', '💦'])
        coin_e = self.bot.config['emotes']['coin']

        #! Send the embed
        msg = await ctx.send(embed=utils.SpecialEmbed(title=f"{emoji} This is your {day.daily:,}x daily in a row! {emoji}", desc=f"**{xp:,} *XP*\n{round(coins):,}x {coin_e}**", footer=footer))

        #! Premium
        if day.premium == True:
            footer = f"Click a random reward!"
            emoji = choice(['🏴', '🔷', '🔶', '🍄'])
            await msg.add_reaction(emoji)
            check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and x.emoji in ["🔷", "🏴", "🔶", "🍄"]
            r, _ = await self.bot.wait_for('reaction_add', check=check)
            if emoji == "🏴":
                reward = choice([250, 300])

            if emoji == "🔷":
                reward = choice([50, 75])

            if emoji == "🍄":
                reward = choice([150, 200])

            if emoji == "🔶":
                reward = choice([-250, -500])

            await msg.edit(embed=utils.SpecialEmbed(title=f"This is your {day.daily:,}x daily in a row!", desc=f"**{xp:,} *XP*\n{round(coins):,}x {coin_e}**", footer=f" {emoji} Extra reward of {reward:,} coins!"))
            c.coins += reward

        #! Save data changes
        day.last_daily = dt.utcnow()
        await msg.clear_reactions()
        async with self.bot.database() as db:
            await day.save(db)
            await c.save(db)
            await lvl.save(db)



def setup(bot):
    x = Daily(bot)
    bot.add_cog(x) 
