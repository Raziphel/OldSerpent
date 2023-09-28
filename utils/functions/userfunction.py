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
            msg = await channel.send(embed=utils.LogEmbed(type="positive", title=f"🎉 level up!", desc=f"{user.mention} is now level: **{lvl.level:,}**\nGranting them: **{round(amount):,}x** {coin}"))

        coin_logs = cls.bot.get_channel(cls.bot.config['channels']['coin_logs'])
        await coin_logs.send(f"**{user.name}** leveled up and is now level **{lvl.level:,}**\nGranting them: **{round(amount):,}x** {coin}")

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
            45: "Sorcerer (Lvl 45)",
            40: "Cleric (Lvl 40)",
            35: "Paladin (Lvl 35)",
            30: "Adventurer (Lvl 30)",
            25: "Warrior (Lvl 25)",
            20: "Hunter (Lvl 20)",
            15: "Villager (Lvl 15)",
            10: "Beggar (Lvl 10)",
            5: "Nit-Wit (Lvl 5)",
            0: "Sacrifice (Lvl 1)",
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
            try:
                role = utils.DiscordGet(guild.roles, name=role_to_add)
                await user.add_roles(role, reason="Adding Level Role.")
            except: 
                print(f'Failed to apply level role: {user.name} getting role: {role_to_add}')





    @classmethod
    async def verify_user(cls, user, type):
        '''Litterally verify someone'''
        guild = cls.bot.get_guild(cls.bot.config['garden_id'])

        if type == "guild":
            verified = utils.DiscordGet(guild.roles, id=cls.bot.config['roles']['janitor'])
            s1 = utils.DiscordGet(guild.roles, id=cls.bot.config['seperator_roles']['access'])
            s2 = utils.DiscordGet(guild.roles, id=cls.bot.config['seperator_roles']['purchases'])
            s3 = utils.DiscordGet(guild.roles, id=cls.bot.config['seperator_roles']['pings'])
            s4 = utils.DiscordGet(guild.roles, id=cls.bot.config['seperator_roles']['bio'])
            await user.add_roles(verified, reason="Verification")
            await user.add_roles(s1, reason="Verification")
            await user.add_roles(s2, reason="Verification")
            await user.add_roles(s3, reason="Verification")
            await user.add_roles(s4, reason="Verification")
            general = cls.bot.get_channel(cls.bot.config['channels']['general'])
            try:
                await general.send(content=f"<@&1134574155828838560> {user.mention}", embed=utils.SpecialEmbed(description=f"Please welcome {user.mention} to the garden!\nBe sure to go to <id:customize> as there is still a lot more roles you choose from!\n\nIf you joined from the **SCP Servers** be sure to check <#1052823837416357999>!\nAbsolutely read the <#856449403173994536> and the <#1133002668189700116> as well for information related to our Discord!", thumbnail=user.avatar.url, footer=" "))
            except: pass
            return

        elif type == "alliance":
            verified = utils.DiscordGet(guild.roles, id=cls.bot.config['roles']['ussy'])
            await user.add_roles(verified, reason="Verification")
            general = cls.bot.get_channel(cls.bot.config['channels']['kingussy'])
            await general.send(embed=utils.SpecialEmbed(description=f"New alliance member joined!\nWelcome {user.mention}!", thumbnail=user.avatar.url))
            return

        elif type == "cultist":
            verified = utils.DiscordGet(guild.roles, id=cls.bot.config['roles']['cultist'])
            await user.add_roles(verified, reason="Cultist Verification")
            general = cls.bot.get_channel(1095761206486237254)
            await general.send(embed=utils.SpecialEmbed(description=f"**A new Cultist has joined!**\nWelcome {user.mention}!\n\nThe cult is mostly just a little secret group for people close to Razi!", thumbnail=user.avatar.url))
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

