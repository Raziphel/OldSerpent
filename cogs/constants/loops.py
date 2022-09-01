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
        playing = choice(["with fire."])
        await self.bot.change_presence(activity=Game(name=playing)) 
        
        #* Setting the Channel Stats.
        members_channel = self.bot.get_channel(856451508865466368)
        gold_coins_channel = self.bot.get_channel(1012200477129191516)
        good_coins_channel = self.bot.get_channel(1012921948575105055)
        evil_coins_channel = self.bot.get_channel(1012922006360035398)
        members = len(set(self.bot.get_all_members()))
        total_gold = utils.Currency.get_total_gold()
        total_good = utils.Currency.get_total_good()
        total_evil = utils.Currency.get_total_evil()
        await members_channel.edit(name=f"Members: {members:,}")
        await gold_coins_channel.edit(name=f"Total Gold: {math.floor(total_gold):,}")
        await good_coins_channel.edit(name=f"Total Good: {math.floor(total_good):,}")
        await evil_coins_channel.edit(name=f"Total Evil: {math.floor(total_evil):,}")


        #! Fixing Adult roles.
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        
        #! get the varible roles!
        adult_furry = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_furry'])
        furry = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['furry'])
        adult_member = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_member'])
        member = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['member'])
        ussy = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['ussy'])
        adult_ussy = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_ussy'])
        nsfw_adult = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nsfw_adult'])
        adult = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult'])
        library_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nsfw_adult'])
        adult_library_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_library_pass'])
        for user in guild.members:
            try:
                mod = utils.Moderation.get (user.id)
                #? Set child & Adults in DB
                if child in user.roles: 
                    mod.child = True
                if adult in user.roles: 
                    mod.adult = True
                if nsfw_adult in user.roles: 
                    mod.adult = True
                async with self.bot.database() as db:
                    await mod.save(db)
                #! Fix adult roles
                if nsfw_adult in user.roles:
                    #? Fixing Furry's NSFW
                    if furry in user.roles:
                        await user.add_roles(adult_furry, reason="Fixing Adult & Furry role.")
                        await user.remove_roles(furry, reason="Fixing Adult & Furry role.")
                    #? Fixing Member's NSFW
                    if member in user.roles:
                        await user.add_roles(adult_member, reason="Fixing Adult & Member role.")
                        await user.remove_roles(member, reason="Fixing Adult & Member role.")
                    #? Fixing Ussy's NSFW
                    if ussy in user.roles:
                        await user.add_roles(adult_ussy, reason="Fixing Adult & ussy role.")
                        await user.remove_roles(ussy, reason="Fixing Adult & Ussy role.")
                    #? Fixing library Pass's NSFW
                    if library_pass in user.roles:
                        await user.add_roles(adult_library_pass, reason="Fixing Adult & Library Pass role.")
                        await user.remove_roles(library_pass, reason="Fixing Adult & Library Pass role.")
            except: pass


        #* Levels Leaderboard
        channel = self.bot.get_channel(self.bot.config['channels']['leaderboard'])
        msg = await channel.fetch_message(1012924362128621608)

        #* Set up the embed
        embed = Embed(color=0x8f00f8)
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
            else: ranks = sorted_rank[:10]
        # users = [self.bot.get_user(i.user_id) for i in ranks]
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 Lvl.{math.floor(rank.level):,}")
        embed.add_field(name='Level Rank', value='\n'.join(text), inline=True)

        await msg.edit(content=f"**If you're on this list your gay. Not Butts.**", embed=embed)


        #! Gold Leaderboard
        msg = await channel.fetch_message(1012924373474213999)

        # Set up the embed
        embed = Embed(color=0x8f00f8)
        embed.set_author(name="The Gold Leaderboard")
        embed.set_footer(text="The shiny stuff!?")

        sorted_rank = utils.Currency.sort_gold_coins()
        ranks = sorted_rank[:10]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.gold_coins):,} Gold Coins")
        embed.add_field(name='Gold Coin Rank', value='\n'.join(text), inline=True)
        await msg.edit(content=" ", embed=embed)

        #! Good Leaderboard
        msg = await channel.fetch_message(1012924390490513539)

        # Set up the embed
        embed = Embed(color=0x8f00f8)
        embed.set_author(name="The Good Leaderboard")
        embed.set_footer(text="The Holy Stuff!?")

        sorted_rank = utils.Currency.sort_good_coins()
        ranks = sorted_rank[:10]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.good_coins):,} Good Coins")
        embed.add_field(name='Good Coin Rank', value='\n'.join(text), inline=True)
        await msg.edit(content=" ", embed=embed)

        #! Evil Leaderboard
        msg = await channel.fetch_message(1012924398124150894)

        # Set up the embed
        embed = Embed(color=0x8f00f8)
        embed.set_author(name="The Evil Coin Leaderboard")
        embed.set_footer(text="You shouldn't have these.")

        sorted_rank = utils.Currency.sort_evil_coins()
        ranks = sorted_rank[:10]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.evil_coins):,} Evil Coins")
        embed.add_field(name='Evil Coin Rank', value='\n'.join(text), inline=True)
        await msg.edit(content=" ", embed=embed)



    @one_min_loop.before_loop
    async def before_one_min_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""
        
        await self.bot.wait_until_ready()





    @tasks.loop(minutes=60)
    async def one_hour_loop(self):
        """The loop that handles updating things every 60 minutes."""

        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t1supporter'])
        goldcoin = "<:GoldCoin:1011145571240779817>"
        goodcoin = "<:GoodCoin:1011145572658446366>"
        evilcoin = "<:EvilCoin:1011145570112512051>"

        t = utils.Timers.get(self.bot.config['razisrealm_id'])
        if (t.last_nitro_reward + timedelta(days=30)) <= dt.utcnow():
            t.last_nitro_reward = dt.now()
            for user in guild.members:
                if nitro in user.roles:
                    c = utils.Currency(user.id)
                    try:
                        await user.send(embed=utils.SpecialEmbed(title="- Nitro Booster Coin Reward -", desc=f"A small reward for being a nitro booster!\n\n**+500 {goldcoin}**\n**+5 {goodcoin}**\n**+5 {evilcoin}**", footer=f"You can expect this reward every 30 days!"))
                    except: pass
                    c.coins += 500
                    c.good_coins += 50
                    c.evil_coins += 1
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
