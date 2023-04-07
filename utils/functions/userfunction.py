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

        #* Emojis
        coin = "<:Coin:1026302157521174649>"

        RNG = choice([1.25, 1.30, 1.35, 1, 0.75, 0.85, 0.9])

        lvl.level += 1
        amount = (lvl.level*500) * RNG
        await utils.CoinFunctions.earn(earner=user, amount=amount)

        lvl.exp = 0
        async with cls.bot.database() as db:
            await lvl.save(db)

        await cls.check_level(user=user)

        if channel:
            msg = await channel.send(embed=utils.LogEmbed(type="positive", title=f"🎉 level up!", desc=f"{user.mention} is now level: **{lvl.level:,}**\nGranting them: {round(amount):,}x {coin}"))

        coin_logs = cls.bot.get_channel(cls.bot.config['channels']['coin_logs'])
        await coin_logs.send(embed=utils.LogEmbed(type="positive", title=f"🎉 level up!", desc=f"{user.mention} is now level: **{lvl.level:,}**\nGranting them: {round(amount):,}x {coin}"))

        await sleep(6)
        try: await msg.delete()
        except: pass

        return




    @classmethod
    async def determine_required_exp(cls, level:int):
        """Determines how much exp is needed to level up!"""
        if level == 0:
            requiredexp = 10
        elif level < 5:
            requiredexp = level*25
        else:
            requiredexp = round(level**2.75)
        return requiredexp


    @classmethod
    async def check_level(cls, user:Member):
        """Checks the highest level role that the given user is able to receive"""

        # Get the users
        guild = cls.bot.get_guild(cls.bot.config['garden_id'])
        lvl = utils.Levels.get(user.id)

        level_roles = {
            100: "Ancient Serpent Deceiver (Lvl 100)",
            90: "Leviathan (Lvl 90)",
            80: "Cosmic Horror (Lvl 80)",
            70: "Dragon (Lvl 70)",
            65: "Malevolent One (Lvl 65)",
            60: "Oath Taker (Lvl 60)",
            55: "Shadow Priest (Lvl 55)",
            50: "Warlock (Lvl 50)",
            45: "Cleric (Lvl 45)",
            40: "Sorcerer (Lvl 40)",
            35: "Wizard (Lvl 35)",
            30: "Cultist (Lvl 30)",
            25: "Witch (Lvl 25)",
            20: "Acolyte (Lvl 20)",
            15: "Zealot (Lvl 15)",
            10: "Member (Lvl 10)",
            5: "Initiate (Lvl 5)",
            0: "sacrifice (Lvl 1)",
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





    @classmethod
    async def verify_user(cls, user, type):
        '''Litterally verify someone'''
        guild = cls.bot.get_guild(cls.bot.config['garden_id'])

        if type == "guild":
            verified = utils.DiscordGet(guild.roles, id=cls.bot.config['roles']['janitor'])
            await user.add_roles(verified, reason="Verification")
            general = cls.bot.get_channel(cls.bot.config['channels']['general'])
            try:
                await general.send(content=f"{user.mention}", embed=utils.SpecialEmbed(description=f"Please welcome the new scum!", thumbnail=user.avatar.url, footer=" "))
            except: pass
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

