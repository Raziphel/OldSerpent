# Discord
from discord.ext.commands import command, cooldown, BucketType, Cog
from discord import Member, Message, User, TextChannel

import utils

from asyncio import sleep
from random import randint, choice
from math import floor

class UserFunction(object):
    bot = None

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
        phel_e = "<:PhelStone:766123219781419020>"
        silver_e = "<:Silver:766123219761233961>"
        gold_e = "<:GoldIngot:766123219827949596>"
        sapphire_e = "<:Sapphire:766123220201635850>"
        ruby_e = "<:Ruby:766123219928481852>"

        RNG = choice([1.25, 1.30, 1.35, 1, 1, 1])

        #! Yes, this is some crazy varible maddness!  It could be better...
        lvl.level += 1
        if lvl.level <= 50: #! Levels 50: Silver & Gold.
            amount_1 = (lvl.level * RNG)*2
            amount_2 = lvl.level * RNG
            c.silver += amount_1
            c.gold += amount_2
            emoji_1 = silver_e
            emoji_2 = gold_e
        elif lvl.level <= 100: #! Levels 100: Gold and Emeralds.
            amount_1 = (lvl.level*0.90) * RNG
            amount_2 = (lvl.level-25) * RNG
            c.gold += amount_1
            c.emerald += amount_2
            emoji_1 = gold_e
            emoji_2 = emerald_e
        elif lvl.level <= 150: #! Levels 150: Emerald and Diamonds.
            amount_1 = (lvl.level*0.80) * RNG
            amount_2 = (lvl.level-50) * RNG
            c.emerald += amount_1
            c.diamond += amount_2
            emoji_1 = emerald_e
            emoji_2 = diamond_e
        elif lvl.level <= 200: #! Levels 200: Diamond and Rubys.
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
            channel = user
            vc = f"**Leveled From being in vc!**"
            await channel.send(content=vc, embed=utils.SpecialEmbed(title=f"🎉{user.name} Is Level {lvl.level:,}!", desc=f"You were rewarded: **{round(amount_1):,}x {emoji_1} {round(amount_2):,}x {emoji_2}**", footer=f"Leveled up in: {user.guild}", guild=user.guild))
        else:
            await channel.send(embed=utils.SpecialEmbed(title=f"🎉{user.name} Is Level {lvl.level:,}!", desc=f"You were rewarded: **{round(amount_1):,}x {emoji_1} {round(amount_2):,}x {emoji_2}**", footer=" ", guild=user.guild))

        log = await utils.ChannelFunction.get_log_channel(guild=user.guild, log="currency")
        await log.send(embed=utils.LogEmbed(type="positive", title=f"🎉{user.name} level up!", desc=f"Now level: **{lvl.level:,} ~~~ {round(amount_1):,}x {emoji_1} {round(amount_2):,}x {emoji_2}**", guild=user.guild))

        return




    @classmethod
    async def determine_required_exp(cls, level:int):
        """Determines how much exp is needed to level up!"""
        if level == 0:
            requiredexp = 10
        elif level < 5:
            requiredexp = level*25
        else:
            requiredexp = round(level**3.35)
        return requiredexp




    @classmethod
    async def verify_user(cls, user, guild):
        '''Litterally verify someone'''
        if guild.id == cls.bot.config['guilds']['RaziRealmID']:
            verified = utils.DiscordGet(guild.roles, name="🎀")
            await user.add_roles(verified, reason="Verification")
            general = cls.bot.get_channel(cls.bot.config['channels']['realm']['sfw_general'])
            await general.send(embed=utils.SpecialEmbed(description=f"Please welcome the new scum, {user.mention}!", thumbnail=user.avatar_url))
            return

        elif guild.id == cls.bot.config['guilds']['FurryRoyaleID']:
            verified = utils.DiscordGet(guild.roles, name="★Please Verify Cutie★")
            await user.remove_roles(verified, reason="Verification")
            general = cls.bot.get_channel(cls.bot.config['channels']['royale']['sfw_general'])
            await general.send(embed=utils.SpecialEmbed(description=f"Please welcome the new scum, {user.mention}!", thumbnail=user.avatar_url))
            return







    # @classmethod
    # async def check_level(cls, user:Member):
    #     """Checks the highest level role that the given user is able to receive"""

    #     # Get the users
    #     guild = cls.bot.get_guild(cls.bot.config['RaziRealmID'])
    #     lvl = utils.Levels.get(user.id)

    #     level_roles = {
    #         55: "Hash Shlinging Slasher ▪️ (Lvl 55)",
    #         50: "Femboy Grim Reaper ▪️ (Lvl 50)",
    #         45: "Magical Unicorn ▪️ (Lvl 45)",
    #         40: "Rainbow Chameleon ▪️ (Lvl 40)",
    #         35: "Giant Catapiller ▪️ (Lvl 35)",
    #         30: "Ice Pheonix ▪️ (Lvl 30)",
    #         25: "Thunder Pigeon ▪️ (Lvl 25)",
    #         20: "Flying JellyFish ▪️ (Lvl 20)",
    #         15: "Cute Puppy ▪️ (Lvl 15)",
    #         10: "Water Spirit ▪️ (Lvl 10)",
    #         5: "Rat ▪️ (Lvl 5)",
    #         1: "Mouse ▪️ (Lvl 1)",
    #     }

    #     # Get roles from the user we'd need to delete
    #     try:
    #         role_to_delete = [i for i in user.roles if i.name in level_roles.values()]
    #     except IndexError:
    #         role_to_delete = None

    #     # Get role that the user is viable to have
    #     viable_level_roles = {i:o for i, o in level_roles.items() if lvl.level >= i}
    #     if viable_level_roles:
    #         role_to_add = viable_level_roles[max(viable_level_roles.keys())]
    #     else:
    #         role_to_add = None

    #     # Add the roles
    #     if role_to_delete:
    #         await user.remove_roles(*role_to_delete, reason="Removing Level Role.")

    #     if role_to_add:
    #         role = utils.DiscordGet(guild.roles, name=role_to_add)
    #         await user.add_roles(role, reason="Adding Level Role.")

