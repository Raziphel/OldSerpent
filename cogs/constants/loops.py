import math
from asyncio import sleep
from datetime import datetime as dt, timedelta
from random import randint, choice

from discord import Game, Embed
from discord.ext import tasks
from discord.ext.commands import Cog

import utils


def format_number(num):
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return f"{num / 1000:.1f} K"
    elif num < 1000000000:
        return f"{num / 1000000:.1f} Mil."
    else:
        return f"{num / 1000000000:.1f} Bil."


class Loops(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.one_min_loop.start()
        self.one_hour_loop.start()
        self.last_members = 0
        self.last_coins = 0
        self.supporters = 0



    @tasks.loop(minutes=1)
    async def one_min_loop(self):
        """The loop that handles updating things every minute."""

        #! Database check
        if self.bot.connected == False:
            await self.bot.change_presence(activity=Game(name="Database is Down!!!"))
            return

        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild

        
        wanting_adult = utils.DiscordGet(guild.roles, id=1070572419254853694)
        for member in guild.members:
            if wanting_adult in member.roles:
                try:
                    await self.bot.get_cog('Verification').verify_adult(author=member, guild=guild)
                except: pass
                wanting_adult = utils.DiscordGet(guild.roles, id=1070572419254853694)
                await member.remove_roles(wanting_adult, reason="Removed wanting adult role")

        #* Setting the bot status.
        playing = choice(["Convincing Eve to eat an apple!", "Slitherin' in the Garden...", "Commiting Atrocities.", "Starting Plagues", "Worshipin' The Bearer of light", "Devilish intentions!"])
        await self.bot.change_presence(activity=Game(name=playing))

        #* Setting the Channel Stats.
        members_channel = self.bot.get_channel(856451508865466368)
        coins_channel = self.bot.get_channel(1047682198523875399)
        supp_channel = self.bot.get_channel(1052050250887598180)
        supporters = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['supporters'])
        nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nitro'])
        members = len(set(self.bot.get_all_members()))
        total_coins = format_number(utils.Currency.get_total_coins())
        total_scps = 0
        for user in guild.members:
            if supporters in user.roles:
                total_scps += 1
            elif nitro in user.roles:
                total_scps += 1


        if self.last_members != members:
            await members_channel.edit(name=f"Members: {members:,}")
            self.last_members = members
        if self.last_coins != total_coins:
            await coins_channel.edit(name=f"Coins: {total_coins}")
            self.last_coins = total_coins
        if self.supporters != supporters:
            await supp_channel.edit(name=f"Supporters: {total_scps:,}")
            self.supporters = supporters


        #* Levels Leaderboard
        channel = self.bot.get_channel(self.bot.config['channels']['leaderboard'])
        msg = await channel.fetch_message(1050324838721523782)

        #* Set up the embed
        embed = Embed(color=randint(1, 0xffffff))
        embed.set_author(name="Welcome to the Server's Leaderboard")
        embed.set_footer(text="if you ain't on here ya trash, sorry.")

        #* Add in level rankings
        sorted_rank = utils.Levels.sort_levels()
        ranks = sorted_rank[:15]
        users = []
        for i in sorted_rank:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 Lvl.{math.floor(rank.level):,}")
        embed.add_field(name='Level Rank', value='\n'.join(text), inline=True)

        await msg.edit(content=f"**Those with the Highest Levels!**", embed=embed)


        #! Coin Leaderboard
        msg = await channel.fetch_message(1050324845986066493)

        # Set up the embed
        embed = Embed(color=randint(1, 0xffffff))
        embed.set_author(name="The Coin Leaderboard")
        embed.set_footer(text="Those with the most coins!")

        sorted_rank = utils.Currency.sort_coins()
        ranks = sorted_rank[:15]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            text.append(f"#{index+1} **{user}** 〰 {math.floor(rank.coins):,} {self.bot.config['emotes']['coin']}")
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

        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild



        #! THE STICKY CODE BLOCK >:O
        lounge = guild.get_channel(807828084937850921) #? General Channel
        adult_lounge = guild.get_channel(1022373213520547912) #? adult lounge Channel
        furry_lounge = guild.get_channel(1028881630363926568) #? furry lounge Channel
        supporter_lounge = guild.get_channel(1056775863842111488) #? supporter lounge Channel
        scp_lounge = guild.get_channel(1056048682878910534) #? scp lounge Channel
        bot_usage = guild.get_channel(1028771493179560066) #? bot_usage Channel
        issues = guild.get_channel(1056747603829731338) #? issues Channel
        supporter = guild.get_channel(1051738903666769950) #? Supporter Channel
        adult_memes = guild.get_channel(1069887003094683698) #? Adult Memes Channel
        channels = [adult_lounge, bot_usage, issues, supporter, adult_memes]
        lounges = [lounge, scp_lounge, supporter_lounge, furry_lounge]
        last_message = None
        for channel in channels:
            message_list = await channel.history(limit=1).flatten()
            try:
                last_message = message_list[0] #? get last message
            except IndexError:
                # no messages in the channel
                print(f'No message in channel? {channel}')
                continue

            #? Check its not the last message already.
            sti = utils.Sticky.get(channel.id)
            if last_message.id == sti.message_id:
                continue
            else:
                try:
                    msg = await channel.fetch_message(sti.message_id)
                    await msg.delete()
                except:  # Unable to delete message
                    pass

                msg = await channel.send('**Loading sticky message**')
                sti.message_id = msg.id

                # ! SAVE THAT SHIT
                async with self.bot.database() as db:
                    await sti.save(db)

                t1 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t1'])
                t2 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t2'])
                t3 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t3'])
                profit = 0
                t1s = 0
                t2s = 0
                t3s = 0
                for user in guild.members:
                    if t1 in user.roles:
                        profit += 9
                        t1s += 1
                    elif t2 in user.roles:
                        profit += 18
                        t2s += 1
                    elif t3 in user.roles:
                        profit += 27
                        t3s += 1

                #? Check the channels sticky!
                if channel == supporter:
                    embed=Embed(title=f"**[- Supporter Sticky -]**",
                    description=f"**This channel displays any type of support shown to the Serpent's Garden!**\nThank you to everyone who chooses to support the server!\n\n<:nitro:1012165382901092462> `These are Nitro Boosters`\n<:Emerald:1094208934979584032> `These are 10$ Supporters` - {t1s} of them!\n<:Diamond:1094208933079564308> `These are 20$ Supporters` - {t2s} of them!\n<:Ruby:1094208936443383930> `These are 30$ Supporters` - {t3s} of them!\n\n**For Serpent's Garden to be self sustaining**\nWe'd need to reach this goal: `{profit}$ / 200$` (Keep in mind Discord takes a cut.)\n\n*But don't worry!  There is no plans of taking Serpent's Garden down for not reaching goal anytime soon! <3*", color=randint(1, 0xffffff))
                if channel == bot_usage:
                    embed=Embed(title=f"**[- Bot Usage Sticky -]**",
                    description=f"**This channel is only for using bot commands!**\nthe Serpent bot has the `/` prefix for regular commands.\nThe Serpent's Music commands use the prefix `!` and both have a help command!", color=randint(1, 0xffffff))
                if channel == adult_lounge:
                    embed=Embed(title=f"**[- Adult Lounge Sticky -]**",
                    description=f"**This channel is only for adults**\n\n**NSFW content is allowed!**\n**Only art/drawn nsfw!  No IRL porn is allowed.**", color=randint(1, 0xffffff))
                if channel == adult_memes:
                    embed=Embed(title=f"**[- Adult Memes Sticky -]**",
                    description=f"**This channel is only for adults**\n\n**NSFW content is allowed!**\n**Only art/drawn nsfw!  No IRL porn is allowed.**", color=randint(1, 0xffffff))
                if channel == issues:
                    embed=Embed(title=f"**[- Issues Sticky -]**",
                    description=f"**This channel is for pinging staff about issues happening the SCP servers!**\n*Please follow these guidelines before you ping!*\n\n**@05 Council** - Ping for Major bugs or anything if you think its important enough.\n**@Game Staff** - Ping for anything SCP Server related.\n**@Discord Staff** - Ping for anything Discord related.", color=randint(1, 0xffffff))
                # if channel in lounges:
                #     embed=Embed(title=f"**[- Lounge Stickys! -]**",
                #     description=f"**Check out the new roles and channel tab at the top of the channels list!**\n\nLounge stickys are updated occasionally to help with any changes", color=randint(1, 0xffffff))
                try:
                    await msg.edit(content=f" ", embed=embed)
                except: 
                    print(f'Couldnt edit sticky for {channel}')




        #* AUTO ROLE FIXING
        child = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['child'])
        adult_furry = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_furry'])
        furry = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['furry'])
        nsfw_adult = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nsfw_adult'])
        adult = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult'])
        library_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['library_pass'])
        adult_library_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult_library_pass'])
        #! get the scp roles!
        supporters = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['supporters'])
        nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nitro'])
        t1 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t1'])
        t2 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t2'])
        t3 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t3'])

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

                #! Fix roles
                await sleep(0.05) #? Causes a huge sharp in cpu why not spread it out.
                if mod.adult == True:
                    #? Fixing library Pass's NSFW
                    if library_pass in user.roles:
                        await user.add_roles(adult_library_pass, reason="Fixing Adult & Library Pass role.")
                        await user.remove_roles(library_pass, reason="Fixing Adult & Library Pass role.")
                    #? Fixing furry's NSFW
                    if furry in user.roles:
                        await user.add_roles(adult_furry, reason="Fixing Adult & furry role.")
                        await user.remove_roles(furry, reason="Fixing Adult & furry role.")

            except Exception as e: print(f'Error fixing roles :: {e}')









        # nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nitro'])
        # coin = "<:Coin:1026302157521174649>"

        # t = utils.Timers.get(self.bot.config['garden_id'])
        # if (t.last_nitro_reward + timedelta(days=30)) <= dt.utcnow():
        #     t.last_nitro_reward = dt.utcnow()
        #     for user in guild.members:
        #         if nitro in user.roles:
        #             c = utils.Currency(user.id)
        #             try:
        #                 await user.send(embed=utils.SpecialEmbed(title="- Nitro Booster Coin Reward -", desc=f"A small reward for being a nitro booster!\n\n**{coin} 5,000x**", footer=f"You can expect this reward every 30 days!"))
        #             except: pass
        #             c.coins += 5000
        #             c.xp += 1000
        #             async with self.bot.database() as db:
        #                 await t.save(db)
        #                 await c.save(db)
        #             print('Handed out Boost rewards')













    @one_hour_loop.before_loop
    async def before_one_hour_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""

        await self.bot.wait_until_ready()





def setup(bot):
    x = Loops(bot)
    bot.add_cog(x)
