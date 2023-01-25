# Discord
from datetime import datetime as dt, timedelta
from random import choice

from discord.ext.commands import command, Cog, ApplicationCommandMeta

import utils


class Daily(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        application_command_meta=ApplicationCommandMeta(),
    )
    async def daily(self, ctx):
        """Claim you daily rewards!"""
        # ! Define variables
        day = utils.Daily.get(ctx.author.id)
        lvl = utils.Levels.get(ctx.author.id)
        c = utils.Currency.get(ctx.author.id)
        if not day.premium:
            footer = " ~ Hasn't unlocked Bonus Rewards ~"
        else:
            footer = "Click a reward!"

        # ! Check if it's first daily
        if not day.daily:
            day.daily = 1
            day.last_daily = (day.last_daily - timedelta(days=5))
        # ! Check if already claimed
        if (day.last_daily + timedelta(hours=22)) >= dt.utcnow():
            tf = day.last_daily + timedelta(hours=22)
            t = dt(1, 1, 1) + (tf - dt.utcnow())

            return await ctx.interaction.response.send_message(
                embed=utils.DefualtEmbed(
                    description=f"You can claim your daily rewards in {t.hour} hours and {t.minute} minutes!"
                )
            )

        # ! Missed daily
        elif (day.last_daily + timedelta(days=3)) <= dt.utcnow():
            day.daily = 1
        # ! Got daily
        elif (day.last_daily + timedelta(hours=22)) <= dt.utcnow():
            day.daily += 1

        rng = choice([1, 1.25, 1.5, 1.75, 2, 3])
        rarity = "Common"
        if rng == 1:
            "Common"
        elif rng == 1.25:
            rarity = "Uncommon"
        elif rng == 1.5:
            rarity = "Rare"
        elif rng == 1.75:
            rarity = "Epic"
        elif rng == 2:
            rarity = "Legendary"
        elif rng == 3:
            rarity = "Mythic"

        # ! Determine reward variables
        if day.daily >= 365:
            daily = 365
        else:
            daily = day.daily
        coins = round((100 + daily) * rng)
        coins = await utils.CoinFunctions.pay_tax(payer=ctx.author, amount=coins)
        c.coins += coins

        # ! Add xP!
        xp = round((lvl.level * 2.25) * rng)
        lvl.exp += xp

        coin_e = self.bot.config['emotes']['coin']

        # ! Send the embed
        msg = await ctx.interaction.response.send_message(
            embed=utils.SpecialEmbed(
                title=f" This is your {day.daily:,}x daily in a row!",
                desc=f"**{rarity} Reward!**\n{xp:,} *XP*\n{round(coins):,}x {coin_e}",
                footer=footer
            )
        )

        # ! Premium
        if day.premium:
            footer = f"Click a random reward!"
            e_emoji = choice(['🏴', '🔷', '🔶', '🍄'])
            emoji = e_emoji
            await msg.add_reaction(e_emoji)
            check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and x.emoji in ["🔷", "🏴", "🔶", "🍄"]
            r, _ = await self.bot.wait_for('reaction_add', check=check)
            if e_emoji == "🏴":
                if emoji == '🏴':
                    reward = choice([1000, 700])

            if e_emoji == "🔷":
                if emoji == '🔷':
                    reward = choice([300, 500])

            if e_emoji == "🍄":
                if emoji == '🍄':
                    reward = choice([200, 400])

            if e_emoji == "🔶":
                if emoji == '🔶':
                    reward = choice([-1000, -500])

            await msg.edit(
                embed=utils.SpecialEmbed(
                    title=f"This is your {day.daily:,}x daily in a row!",
                    desc=f"**{rarity} Reward!**\n{xp:,} *XP*\n{round(coins):,}x {coin_e}",
                    footer=f" {emoji} Extra reward of {reward:,} coins!"
                )
            )
            c.coins += reward

        # ! Save data changes
        day.last_daily = dt.utcnow()
        await msg.clear_reactions()
        async with self.bot.database() as db:
            await day.save(db)
            await c.save(db)
            await lvl.save(db)


def setup(bot):
    x = Daily(bot)
    bot.add_cog(x)
