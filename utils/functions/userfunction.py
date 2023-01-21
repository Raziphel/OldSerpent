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
        coin = "<:Coin:1026302157521174649>"

        RNG = choice([1.25, 1.30, 1.35, 1, 0.75, 0.85, 0.9])

        lvl.level += 1
        amount = (lvl.level*500) * RNG
        amount = await utils.CoinFunctions.pay_tax(payer=user, amount=amount)
        c.coins += amount
        lvl.exp = 0
        async with cls.bot.database() as db:
            await c.save(db)
            await lvl.save(db)

        await cls.check_level(user=user)

        if channel:
            msg = await channel.send(embed=utils.LogEmbed(type="positive", title=f"🎉 level up!", desc=f"{user.mention} is now level: **{lvl.level:,}**\nGranting them: {round(amount):,}x {coin}"))

        levels = cls.bot.get_channel(cls.bot.config['channels']['levels'])
        await levels.send(embed=utils.LogEmbed(type="positive", title=f"🎉 level up!", desc=f"{user.mention} is now level: **{lvl.level:,}**\nGranting them: {round(amount):,}x {coin}"))

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
            100: "Serpent's Hand",
            90: "Gamers Against Weed",
            80: "Chaos Insurgency",
            75: "Children of the Scarlet King",
            70: "Sarkic Cult",
            65: "Church of the Broken God",
            60: "Global Occult Coalition",
            55: "Unusual Incidents Unit",
            50: "Ethics Committee",
            45: "Memetics Division",
            40: "Site Director",
            35: "Facility Manager",
            30: "MTF Operative",
            25: "Security Officer",
            20: "Containment Specialist",
            15: "Head-Researcher",
            10: "Scientist",
            5: "D-Class",
            0: "Janitor",
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
                await general.send(embed=utils.SpecialEmbed(description=f"Please welcome the new scum, {user.mention}!", thumbnail=user.avatar.url))
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

