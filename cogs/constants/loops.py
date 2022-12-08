from datetime import datetime as dt, timedelta
from random import choice

from discord.ext.commands import Cog
from discord.ext import tasks
from discord import Member, Message, User, Game, Embed, Color

import math
from random import randint, choice

from asyncio import sleep

import utils

class Loops(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.one_min_loop.start()
        self.one_hour_loop.start()
        self.last_members = 0
        self.last_coins = 0


    @tasks.loop(minutes=1)
    async def one_min_loop(self):
        """The loop that handles updating things every minute."""

        #! Databse check
        if self.bot.connected == False:
            await self.bot.change_presence(activity=Game(name="Databse is Down!!!")) 
            return

        #* Setting the bot status.
        playing = choice(["75% Complete"])
        await self.bot.change_presence(activity=Game(name=playing)) 

        #* Setting the Channel Stats.
        members_channel = self.bot.get_channel(856451508865466368)
        coins_channel = self.bot.get_channel(1047682198523875399)
        members = len(set(self.bot.get_all_members()))
        total_coins = utils.Currency.get_total_coins()
        if self.last_members != members:
            await members_channel.edit(name=f"Members: {members:,}")
            self.last_members = members
        if self.last_coins != total_coins:
            await coins_channel.edit(name=f"Coins: {math.floor(total_coins):,}")
            self.last_coins = total_coins

        #! Fixing Adult roles.
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild

        #! get the varible roles!
        child = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['child'])
        adult_furry = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_furry'])
        furry = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['furry'])
        nsfw_adult = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nsfw_adult'])
        adult = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult'])
        # library_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nsfw_adult'])
        # adult_library_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_library_pass'])
        light_zone = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['light_zone'])
        adult_light_zone = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_light_zone'])

        for user in guild.members:
            try: #! Fixing adults roles
                mod = utils.Moderation.get(user.id)
                #? Set child & Adults in DB
                if child in user.roles: 
                    if mod.child == False:
                        mod.child = True
                        mod.adult = False
                if adult in user.roles: 
                    if mod.adult == False:
                        mod.adult = True
                        mod.child = False
                if nsfw_adult in user.roles:
                    if mod.adult == False:
                        mod.adult = True
                        mod.child = False
                async with self.bot.database() as db:
                    await mod.save(db)

                #! Fix adult roles
                if nsfw_adult in user.roles:
                    #? Fixing Furry's NSFW
                    if furry in user.roles:
                        await user.add_roles(adult_furry, reason="Fixing Adult & Furry role.")
                        await user.remove_roles(furry, reason="Fixing Adult & Furry role.")
                    # #? Fixing library Pass's NSFW
                    # if library_pass in user.roles:
                    #     await user.add_roles(adult_library_pass, reason="Fixing Adult & Library Pass role.")
                    #     await user.remove_roles(library_pass, reason="Fixing Adult & Library Pass role.")
            except Exception as e: print(f'Error fixing roles :: {e}')

        #* Levels Leaderboard
        channel = self.bot.get_channel(self.bot.config['channels']['leaderboard'])
        msg = await channel.fetch_message(1012924362128621608)

        #* Set up the embed
        embed = Embed(color=randint(1, 0xffffff))
        embed.set_author(name="Welcome to the Server's Leaderboard")
        embed.set_footer(text="if you ain't on here ya trash, sorry.")

        #* Add in level rankings
        sorted_rank = utils.Levels.sort_levels()
        ranks = sorted_rank[:20]
        users = []
        for i in sorted_rank:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
            else: ranks = sorted_rank[:20]
        # users = [self.bot.get_user(i.user_id) for i in ranks]
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 Lvl.{math.floor(rank.level):,}")
        embed.add_field(name='Level Rank', value='\n'.join(text), inline=True)

        await msg.edit(content=f"**Those with the Highest Levels!**", embed=embed)


        #! Coin Leaderboard
        msg = await channel.fetch_message(1012924373474213999)

        # Set up the embed
        embed = Embed(color=randint(1, 0xffffff))
        embed.set_author(name="The Coin Leaderboard")
        embed.set_footer(text="Those with the most coins!")

        sorted_rank = utils.Currency.sort_coins()
        ranks = sorted_rank[:20]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.coins):,} Gold Coins")
        embed.add_field(name='Coin Rank', value='\n'.join(text), inline=True)
        await msg.edit(content=" ", embed=embed)


    @one_min_loop.before_loop
    async def before_one_min_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""
        
        await self.bot.wait_until_ready()





    @tasks.loop(minutes=60)
    async def one_hour_loop(self):
        """The loop that handles updating things every 60 minutes."""

        #? Check if bot is connected!
        if self.bot.connected == False:
            return


        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['thaumiel'])
        coin = "<:Coin:1026302157521174649>"

        t = utils.Timers.get(self.bot.config['razisrealm_id'])
        if (t.last_nitro_reward + timedelta(days=30)) <= dt.utcnow():
            t.last_nitro_reward = dt.now()
            for user in guild.members:
                if nitro in user.roles:
                    c = utils.Currency(user.id)
                    try:
                        await user.send(embed=utils.SpecialEmbed(title="- Nitro Booster Coin Reward -", desc=f"A small reward for being a nitro booster!\n\n**{coin} 5000x**", footer=f"You can expect this reward every 30 days!"))
                    except: pass
                    c.coins += 5000
                    c.xp += 1000
                    async with self.bot.database() as db:
                        await t.save(db)
                        await c.save(db)
                    print('Handed out Boost rewards')




    @one_hour_loop.before_loop
    async def before_one_hour_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""
        
        await self.bot.wait_until_ready()





def setup(bot):
    x = Loops(bot)
    bot.add_cog(x)
