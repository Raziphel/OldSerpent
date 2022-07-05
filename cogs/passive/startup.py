from datetime import datetime as dt, timedelta
from random import choice

from discord.ext.commands import Cog
from discord.ext import tasks
from discord import Member, Message, User, Game, Embed, Color

import math
from random import randint, choice

from asyncio import sleep

import utils

class Startup(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botpres_loop.start()
        self.bot.loop.create_task(self.channel_info())
        self.leaderboard_update_loop.start()



    @tasks.loop(minutes=120)
    async def botpres_loop(self):
        '''updates the bot's presence!'''
        hours = 0
        playing = choice(["...", "Bwahahaha", "Declaring Victory.", "Wondering when you'll show some respect.", "Not doing anything a maid would do.", "Spelling out Destuction...", "Washing away the sins.", "Holding Council meetings!", "Brainwashing the crowd.", "Terrorizing Families.", "Where art thou?", "Generating responses.", "Your nothing more than trash.", "Squashing bugs.", "Praise be the Maiden.", "You will not survive.", "Waiting...", "When the stars align.", "Wasting your time.", "Don't get lost now...", "Am I bot?  Or am I secretly a person...", "Where am I.", "Damn right, I'm at the top!", "Bring it bitches!"])
        await self.bot.change_presence(activity=Game(name=playing)) 
        if hours >= 24:
            self.bot.close()
        hours +=2


    @botpres_loop.before_loop
    async def bot_pres_update(self):
        '''Waits until the cache loads up before running the pres loop'''
        await self.bot.wait_until_ready()



    @tasks.loop(minutes=60)
    async def channel_info(self):
        '''
        updates channel info
        '''
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            members_channel = self.bot.get_channel(856451508865466368)
            members = len(set(self.bot.get_all_members()))
            await members_channel.edit(name=f"Members: 〔{members:,}〕")
            await sleep(10) 


    @channel_info.before_loop
    async def info_update(self):
        '''Waits until the cache loads up before running the pres loop'''
        await self.bot.wait_until_ready()



    @tasks.loop(minutes=5)
    async def leaderboard_update_loop(self):
        """The loop that handles the leaderboard updating"""


        #! Fixing Adult and Furry role.
        guild = self.bot.get_guild(self.bot.config['razisrealm_id'])

        for user in guild.members:
            role = utils.DiscordGet(guild.roles, id=929270825352331265)
            role2 = utils.DiscordGet(guild.roles, id=877449848876572742)
            role3 = utils.DiscordGet(guild.roles, id=702766584715804704)
            if role2 in user.roles:
                if role3 in user.roles:
                    await user.add_roles(role, reason="Fixing Adult & Furry role.")
                    await user.remove_roles(role2, reason="Fixing Adult & Furry role.")


        #! Levels Leaderboard
        channel = self.bot.get_channel(self.bot.config['channels']['leaderboard'])
        msg = await channel.fetch_message(962302873956417547)

        # Set up the embed
        embed = Embed(color=0x8f00f8)
        embed.set_author(name="Welcome to the Server's Leaderboard")
        embed.set_footer(text="if you ain't on here ya trash, sorry.")

        # Add in level rankings
        sorted_rank = utils.Levels.sort_levels()
        ranks = sorted_rank[:10]
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


        #! Emerald Leaderboard
        msg = await channel.fetch_message(962302899931734046)

        # Set up the embed
        embed = Embed(color=0x8f00f8)
        embed.set_author(name="The Emerald Leaderboard")
        embed.set_footer(text="Got some of that green stuff.")

        sorted_rank = utils.Currency.sort_emeralds()
        ranks = sorted_rank[:10]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.emerald):,} Emeralds")
        embed.add_field(name='Emerald Rank', value='\n'.join(text), inline=True)


        await msg.edit(content="**Not that green stuff.**", embed=embed)


        #! Diamond Leaderboard
        msg = await channel.fetch_message(962302909280837652)

        # Set up the embed
        embed = Embed(color=0x8f00f8)
        embed.set_author(name="The Diamond Leaderboard")
        embed.set_footer(text="The shiny stuff!?")

        sorted_rank = utils.Currency.sort_diamonds()
        ranks = sorted_rank[:10]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.diamond):,} Diamonds")
        embed.add_field(name='Diamond Rank', value='\n'.join(text), inline=True)


        await msg.edit(content="**Better to get in minecraft.**", embed=embed)

        #! Ruby Leaderboard
        msg = await channel.fetch_message(962302921658216449)

        # Set up the embed
        embed = Embed(color=0x8f00f8)
        embed.set_author(name="The Ruby Leaderboard")
        embed.set_footer(text="That bloody Gem!?")

        sorted_rank = utils.Currency.sort_ruby()
        ranks = sorted_rank[:10]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.ruby):,} Rubys")
        embed.add_field(name='Ruby Rank', value='\n'.join(text), inline=True)


        await msg.edit(content="**Was almost in minecraft actually!**", embed=embed)


        #! Sapphire Leaderboard
        msg = await channel.fetch_message(962302936577355776)

        # Set up the embed
        embed = Embed(color=0x8f00f8)
        embed.set_author(name="The Sapphire Leaderboard")
        embed.set_footer(text="That Gem of Tears!")

        sorted_rank = utils.Currency.sort_sapphire()
        ranks = sorted_rank[:10]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.sapphire):,} Sapphires")
        embed.add_field(name='Sapphire Rank', value='\n'.join(text), inline=True)


        await msg.edit(content="**Blue and pretty. c;**", embed=embed)

    @leaderboard_update_loop.before_loop
    async def before_leaderboard_update_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""
        
        await self.bot.wait_until_ready()





def setup(bot):
    x = Startup(bot)
    bot.add_cog(x)
