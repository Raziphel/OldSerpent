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
        goldcoin = "<:GoldCoin:1011145571240779817>"
        goodcoin = "<:GoodCoin:1011145572658446366>"
        evilcoin = "<:EvilCoin:1011145570112512051>"

        RNG = choice([1.25, 1.30, 1.35, 1, 1, 1])

        #! Yes, this is some crazy varible maddness!  It could be better...
        lvl.level += 1
        amount_1 = (lvl.level*3) * RNG
        amount_2 = (lvl.level*2) * RNG
        amount_3 = floor(lvl.level/2) * RNG
        c.coins += amount_1
        c.good_coins += amount_2
        c.evil_coins += amount_3
        emoji_1 = goldcoin
        emoji_2 = goodcoin
        emoji_3 = evilcoin

        lvl.exp = 0

        async with cls.bot.database() as db:
            await c.save(db)
            await lvl.save(db)

        if channel == None:
            return
        else:
            msg = await channel.send(embed=utils.SpecialEmbed(title=f"🎉{user.name} Is Level {lvl.level:,}!", desc=f"You were rewarded: **{round(amount_1):,}x {emoji_1}\n {round(amount_2):,}x {emoji_2}\n {round(amount_3):,}x {emoji_3}**", footer=" "))

        try: await cls.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"🎉{user.name} level up!", desc=f"Now level: **{lvl.level:,} ~~~ {round(amount_1):,}x {emoji_1} {round(amount_2):,}x {emoji_2}\n {round(amount_3):,}x {emoji_3}**"))
        except: pass

        await sleep(2)
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
    async def verify_user(cls, user, type):
        '''Litterally verify someone'''
        guild = cls.bot.get_guild(cls.bot.config['razisrealm_id'])

        if type == "guild":
            verified = utils.DiscordGet(guild.roles, id=cls.bot.config['roles']['member'])
            await user.add_roles(verified, reason="Verification")
            general = cls.bot.get_channel(cls.bot.config['channels']['lounge'])
            await general.send(embed=utils.SpecialEmbed(description=f"Please welcome the new scum, {user.mention}!", thumbnail=user.avatar.url))
            return

        elif type == "alliance":
            verified = utils.DiscordGet(guild.roles, id=cls.bot.config['roles']['ussy'])
            await user.add_roles(verified, reason="Verification")
            general = cls.bot.get_channel(cls.bot.config['channels']['kingussy'])
            await general.send(embed=utils.SpecialEmbed(description=f"New alliance member joined!\nWelcome {user.mention}!", thumbnail=user.avatar.url))
            return

        elif type == "furry":
            verified = utils.DiscordGet(guild.roles, id=cls.bot.config['roles']['furry'])
            await user.add_roles(verified, reason="Verification")
            general = cls.bot.get_channel(cls.bot.config['channels']['furry_lounge'])
            await general.send(embed=utils.SpecialEmbed(description=f"A new furry has joined!\nWelcome {user.mention}!", thumbnail=user.avatar.url))
            return

        elif type == "adult":
            verified = utils.DiscordGet(guild.roles, id=cls.bot.config['roles']['nsfw_adult'])
            await user.add_roles(verified, reason="Verification")
            return

        elif type == "kindaadult":
            verified = utils.DiscordGet(guild.roles, id=cls.bot.config['roles']['adult'])
            await user.add_roles(verified, reason="Verification")
            return

        elif type == "notadult":
            verified = utils.DiscordGet(guild.roles, id=cls.bot.config['roles']['child'])
            await user.add_roles(verified, reason="Verification")
            return




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