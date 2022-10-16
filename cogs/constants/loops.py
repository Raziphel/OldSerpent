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


    @tasks.loop(minutes=1)
    async def one_min_loop(self):
        """The loop that handles updating things every minute."""

        #* Setting the bot status.
        playing = choice(["40% Complete"])
        await self.bot.change_presence(activity=Game(name=playing)) 

        #* Setting the Channel Stats.
        members_channel = self.bot.get_channel(856451508865466368)
        coins_channel = self.bot.get_channel(1030001764537217084)
        members = len(set(self.bot.get_all_members()))
        total_coins = utils.Currency.get_total_coins()
        await members_channel.edit(name=f"Members: {members:,}")
        await coins_channel.edit(name=f"Coins: {math.floor(total_coins):,}")

        #! Fixing Adult roles.
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild

        #! get the varible roles!
        child = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['child'])
        adult_furry = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_furry'])
        furry = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['furry'])
        scp = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['scp'])
        adult_scp = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_scp'])
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
                    #? Fixing scp's NSFW
                    if scp in user.roles:
                        await user.add_roles(adult_scp, reason="Fixing Adult & scp role.")
                        await user.remove_roles(scp, reason="Fixing Adult & scp role.")
                    #? Fixing Light Zones's NSFW
                    if light_zone in user.roles:
                        await user.add_roles(adult_light_zone, reason="Fixing Adult & light zone role.")
                        await user.remove_roles(light_zone, reason="Fixing Adult & light zone role.")
                    # #? Fixing library Pass's NSFW
                    # if library_pass in user.roles:
                    #     await user.add_roles(adult_library_pass, reason="Fixing Adult & Library Pass role.")
                    #     await user.remove_roles(library_pass, reason="Fixing Adult & Library Pass role.")
            except Exception as e: print(f'Error fixing roles :: {e}')

        # #* Levels Leaderboard
        # channel = self.bot.get_channel(self.bot.config['channels']['leaderboard'])
        # msg = await channel.fetch_message(1012924362128621608)

        # #* Set up the embed
        # embed = Embed(color=0x8f00f8)
        # embed.set_author(name="Welcome to the Server's Leaderboard")
        # embed.set_footer(text="if you ain't on here ya trash, sorry.")

        # #* Add in level rankings
        # sorted_rank = utils.Levels.sort_levels()
        # ranks = sorted_rank[:20]
        # users = []
        # for i in sorted_rank:
        #     user = self.bot.get_user(i.user_id)
        #     if user != None:
        #         users.append(user)
        #     else: ranks = sorted_rank[:10]
        # # users = [self.bot.get_user(i.user_id) for i in ranks]
        # text = []
        # for index, (user, rank) in enumerate(zip(users, ranks)):
        #     text.append(f"#{index+1} **{user}** 〰 Lvl.{math.floor(rank.level):,}")
        # embed.add_field(name='Level Rank', value='\n'.join(text), inline=True)

        # await msg.edit(content=f"**If you're on this list your gay. Not Butts.**", embed=embed)


        # #! Gold Leaderboard
        # msg = await channel.fetch_message(1012924373474213999)

        # # Set up the embed
        # embed = Embed(color=0x8f00f8)
        # embed.set_author(name="The Gold Leaderboard")
        # embed.set_footer(text="The shiny stuff!?")

        # sorted_rank = utils.Currency.sort_gold_coins()
        # ranks = sorted_rank[:10]
        # users = []
        # for i in ranks:
        #     user = self.bot.get_user(i.user_id)
        #     if user != None:
        #         users.append(user)
        # text = []
        # for index, (user, rank) in enumerate(zip(users, ranks)):
        #     text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.gold_coins):,} Gold Coins")
        # embed.add_field(name='Gold Coin Rank', value='\n'.join(text), inline=True)
        # await msg.edit(content=" ", embed=embed)

        # #! Good Leaderboard
        # msg = await channel.fetch_message(1012924390490513539)

        # # Set up the embed
        # embed = Embed(color=0x8f00f8)
        # embed.set_author(name="The Good Leaderboard")
        # embed.set_footer(text="The Holy Stuff!?")

        # sorted_rank = utils.Currency.sort_good_coins()
        # ranks = sorted_rank[:10]
        # users = []
        # for i in ranks:
        #     user = self.bot.get_user(i.user_id)
        #     if user != None:
        #         users.append(user)
        # text = []
        # for index, (user, rank) in enumerate(zip(users, ranks)):
        #     text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.good_coins):,} Good Coins")
        # embed.add_field(name='Good Coin Rank', value='\n'.join(text), inline=True)
        # await msg.edit(content=" ", embed=embed)

        # #! Evil Leaderboard
        # msg = await channel.fetch_message(1012924398124150894)

        # # Set up the embed
        # embed = Embed(color=0x8f00f8)
        # embed.set_author(name="The Evil Coin Leaderboard")
        # embed.set_footer(text="You shouldn't have these.")

        # sorted_rank = utils.Currency.sort_evil_coins()
        # ranks = sorted_rank[:10]
        # users = []
        # for i in ranks:
        #     user = self.bot.get_user(i.user_id)
        #     if user != None:
        #         users.append(user)
        # text = []
        # for index, (user, rank) in enumerate(zip(users, ranks)):
        #     text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.evil_coins):,} Evil Coins")
        # embed.add_field(name='Evil Coin Rank', value='\n'.join(text), inline=True)
        # await msg.edit(content=" ", embed=embed)



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
        nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t1supporter'])
        coin = "<:Coin:1026302157521174649>"

        t = utils.Timers.get(self.bot.config['razisrealm_id'])
        if (t.last_nitro_reward + timedelta(days=30)) <= dt.utcnow():
            t.last_nitro_reward = dt.now()
            for user in guild.members:
                if nitro in user.roles:
                    c = utils.Currency(user.id)
                    try:
                        await user.send(embed=utils.SpecialEmbed(title="- Nitro Booster Coin Reward -", desc=f"A small reward for being a nitro booster!\n\n**{coin} 500x**", footer=f"You can expect this reward every 30 days!"))
                    except: pass
                    c.coins += 500
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
