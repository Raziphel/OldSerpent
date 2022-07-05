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


    @property  #! The Server logs
    def lounge(self):
        return cls.bot.get_channel(cls.bot.config['channels']['lounge']) 


    #! For level ups!
    @classmethod
    async def level_up(cls, user:Member, channel:TextChannel=None):
        '''Gives a level up'''

        #! Set Varible
        lvl = utils.Levels.get(user.id)
        c = utils.Currency.get(user.id)
        s = utils.Settings.get(user.id)

        RNG = choice([0.50, 0.75, 0.80, 0.95, 1.10, 1.20, 1.25, 1.50])

        diamonds = round((lvl.level*20.0)*RNG) + 3

        lvl.level += 1
        lvl.exp = 0
        c.diamond += diamonds

        async with cls.bot.database() as db:
            await c.save(db)
            await lvl.save(db)

        #! Check level role
        await cls.check_level(user=user)

        vc = f" "
        if channel == None:
            ss = utils.Settings.get(user.id)
            if ss.vc_lvls == True:
                channel = user
                vc = f"**Leveled From being in vc!**"
                msg = await channel.send(content=vc, embed=utils.SpecialEmbed(title=f"🎉{user.name} leved up!", desc=f"Now level {lvl.level}!\nYou were rewarded: **{round(diamonds):,}x** {cls.bot.config['emotes']['diamond']}", footer=f"Leveled up in: {user.guild}"))
        else:
            msg = await channel.send(content=vc, embed=utils.SpecialEmbed(title=f"🎉{user.name} leved up!", desc=f"Now level {lvl.level}!\nYou were rewarded: **{round(diamonds):,}x** {cls.bot.config['emotes']['diamond']}", footer=f""))

        # await cls.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"🎉{user.name} level up!", desc=f"Now level: **{lvl.level:,} ~~~ {round(diamonds):,}x {cls.bot.config['emotes']['diamond']}"))
        await sleep(5)
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