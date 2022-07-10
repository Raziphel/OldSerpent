# Discord
from discord.ext.commands import command, cooldown, BucketType, Cog
from discord import Member, Message, User, TextChannel

import utils

from asyncio import sleep
from random import randint, choice
from math import floor

class UserFunction(object):
    bot = None

    @property  #! The currency logs
    def currency_log(cls):
        return cls.bot.get_channel(cls.bot.config['channels']['currency_log'])


    # For level ups!
    @classmethod
    async def level_up(cls, user:Member, channel:TextChannel=None):
        '''Gives a level up'''

        #! Give first quest
        #q = utils.Quests.get(user.id)
        #if q.q1 == False:
        #    await cls.bot.get_cog('Quests').get_quest(user=user, quest_no=1)

        #! Set Varible
        lvl = utils.Levels.get(user.id)
        c = utils.Currency.get(user.id)

        #* Emojis
        amethyst_e = "<:Amethyst:766123218732843019>"
        diamond_e = "<:Diamond:766123219609976832>"
        emerald_e = "<:Emerald:766123219731611668>"
        phel_e = "<:crimson:766123219781419020>"
        silver_e = "<:Silver:766123219761233961>"
        gold_e = "<:GoldIngot:766123219827949596>"
        sapphire_e = "<:Sapphire:766123220201635850>"
        ruby_e = "<:Ruby:766123219928481852>"

        RNG = choice([1.25, 1.30, 1.35, 1, 1, 1])

        #! Yes, this is some crazy varible maddness!  It could be better...
        lvl.level += 1
        if lvl.level <= 20: #! Levels 20: Silver & Gold.
            amount_1 = (lvl.level * RNG)*2
            amount_2 = lvl.level * RNG
            c.silver += amount_1
            c.gold += amount_2
            emoji_1 = silver_e
            emoji_2 = gold_e
        elif lvl.level <= 40: #! Levels 40: Gold and Emeralds.
            amount_1 = (lvl.level*0.90) * RNG
            amount_2 = (lvl.level-25) * RNG
            c.gold += amount_1
            c.emerald += amount_2
            emoji_1 = gold_e
            emoji_2 = emerald_e
        elif lvl.level <= 60: #! Levels 60: Emerald and Diamonds.
            amount_1 = (lvl.level*0.80) * RNG
            amount_2 = (lvl.level-50) * RNG
            c.emerald += amount_1
            c.diamond += amount_2
            emoji_1 = emerald_e
            emoji_2 = diamond_e
        elif lvl.level <= 80: #! Levels 80: Diamond and Rubys.
            amount_1 = (lvl.level*0.70) * RNG
            amount_2 = (lvl.level-75) * RNG
            c.diamond += amount_1
            c.ruby += amount_2
            emoji_1 = diamond_e
            emoji_2 = ruby_e

        lvl.exp = 0

        async with cls.bot.database() as db:
            await c.save(db)
            await lvl.save(db)

        if channel == None:
            return
        else:
            msg = await channel.send(embed=utils.SpecialEmbed(title=f"🎉{user.name} Is Level {lvl.level:,}!", desc=f"You were rewarded: **{round(amount_1):,}x {emoji_1} {round(amount_2):,}x {emoji_2}**", footer=" ", guild=user.guild))

        await self.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"🎉{user.name} level up!", desc=f"Now level: **{lvl.level:,} ~~~ {round(amount_1):,}x {emoji_1} {round(amount_2):,}x {emoji_2}**", guild=user.guild))

        await sleep(4)
        await msg.delete()

        return




    @classmethod
    async def determine_required_exp(cls, level:int):
        """Determines how much exp is needed to level up!"""
        if level == 0:
            requiredexp = 10
        elif level < 5:
            requiredexp = level*25
        else:
            requiredexp = round(level**2.25)
        return requiredexp




    @classmethod
    async def check_level(cls, user:Member):
        """Checks the highest level role that the given user is able to receive"""

        # Get the users
        guild = cls.bot.get_guild(cls.bot.config['razisrealm_id'])
        lvl = utils.Levels.get(user.id)

        level_roles = {
            100: "Grand Master [100]",
            91: "Master [91-99]",
            81: "Challenger [81-90]",
            61: "King [61~80]",
            41: "Queen [41~60]",
            26: "Bishop [26~40]",
            16: "Rook [16~25]",
            6: "Knight [6~15]",
            0: "Pawn [1~5]",
        }

        # Get roles from the user we'd need to delete
        try:
            role_to_delete = [i for i in user.roles if i.name in level_roles.values()]
        except IndexError:
            role_to_delete = None

        # Get role that the user is viable to have
        viable_level_roles = {i:o for i, o in level_roles.items() if lvl.level >= i}
        if viable_level_roles:
            role_to_add = viable_level_roles[max(viable_level_roles.keys())]
        else:
            role_to_add = None

        # Add the roles
        if role_to_delete:
            await user.remove_roles(*role_to_delete, reason="Removing Level Role.")

        if role_to_add:
            role = utils.DiscordGet(guild.roles, name=role_to_add)
            await user.add_roles(role, reason="Adding Level Role.")