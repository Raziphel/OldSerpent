# Discord
from datetime import datetime as dt, timedelta
from random import choice

import discord
from discord.ext.commands import command, Cog, ApplicationCommandMeta

import utils


class Daily(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  # ! The members logs
    def coin_logs(self):
        return self.bot.get_channel(self.bot.config['channels']['logs']['coins'])  # ?Coins log channel



    @command(
        application_command_meta=ApplicationCommandMeta(),
    )
    async def daily(self, ctx):
        """Claim you daily rewards!"""
        # ! Define variables
        day = utils.Daily.get(ctx.author.id)
        lvl = utils.Levels.get(ctx.author.id)
        c = utils.Currency.get(ctx.author.id)

        # ! Check if it's first daily
        if not day.daily:
            day.daily = 1
            day.last_daily = (dt.utcnow() - timedelta(days=3))
        # ! Check if already claimed
        if (day.last_daily + timedelta(hours=22)) >= dt.utcnow():
            tf = day.last_daily + timedelta(hours=22)
            t = dt(1, 1, 1) + (tf - dt.utcnow())

            return await ctx.interaction.response.send_message(f"**You can claim your daily rewards in {t.hour} hours and {t.minute} minutes!**")

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
        coins = round((10 + (daily*2.7)) * rng)
        await utils.CoinFunctions.earn(earner=ctx.author, amount=coins)

        # ! Add xP!
        xp = round((lvl.level * (2.25+(daily*0.25))) * rng)
        lvl.exp += xp

        coin_e = self.bot.config['emotes']['coin']

        footer = " ~ Hasn't unlocked Bonus Rewards ~"
        components = None

        # ! Premium
        if day.premium:
            footer = "Click for a reward!"
            emojis = (
                "❤",
                "🧡",
                "💛",
                "💚",
                "💙",
                "💜",
                "🤎",
                "🖤",
                "🤍"
            )
            emoji = choice(emojis)
            components = discord.ui.MessageComponents(
                discord.ui.ActionRow(
                    (reward_button := discord.ui.Button(emoji=emoji)),
                ),
            )

        # ! Send the embed
        msg = await ctx.interaction.response.send_message(
            embed=utils.DefaultEmbed(
                title=f" This is your {day.daily:,}x daily in a row!",
                desc=f"**{rarity} Reward!**\n{xp:,} *XP*\n{round(coins):,}x {coin_e}",
                footer=footer
            ),
            components=components
        )
        
        await self.coin_logs.send(f"**{ctx.author}** was Granted **{coins:,} {coin_e}** for his {day.daily:,} daily!")

        if day.premium:
            def check(interaction: discord.Interaction):
                if interaction.user != ctx.author:
                    return False

                return interaction.custom_id == reward_button.custom_id

            # Wait for the user to respond
            interaction = await self.bot.wait_for("component_interaction", check=check)

            reward = choice([50, 100, 150, 200, 250])
            c.coins += reward

            # Now the user has responded, disable the buttons on the message
            components.disable_components()

            await interaction.response.edit_message(
                embed=utils.DefaultEmbed(
                    title=f"This is your {day.daily:,}x daily in a row!",
                    desc=f"**{rarity} Reward!**\n{xp:,} *XP*\n{round(coins):,}x {coin_e}",
                    footer=f" {emoji} Extra reward of {reward:,} coins!"
                ),
                components=components
            )

        # ! Save data changes
        day.last_daily = dt.utcnow()
        async with self.bot.database() as db:
            await day.save(db)
            await lvl.save(db)

        #! Quest 1 Complete
        await self.bot.get_cog('Quests').get_quest(user=ctx.author, quest_no=3, completed=True)


def setup(bot):
    x = Daily(bot)
    bot.add_cog(x)
