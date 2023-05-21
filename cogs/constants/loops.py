from math import floor
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
        self.ten_sec_loop.start()
        self.last_members = 0
        self.last_coins = 0
        self.supporters = 0
        self.serpent_color = "black"





    @tasks.loop(seconds=10)
    async def ten_sec_loop(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild









    @tasks.loop(minutes=1)
    async def one_min_loop(self):
        """The loop that handles updating things every minute."""

        #! Database check
        if self.bot.connected == False:
            await self.bot.change_presence(activity=Game(name="Database is Down!!!"))
            return

        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild

        #+ Wanting Adult Verification!
        wanting_adult = utils.DiscordGet(guild.roles, id=1070572419254853694)
        for member in guild.members:
            if wanting_adult in member.roles:
                await member.remove_roles(wanting_adult, reason="Removed wanting adult role")
                try:
                    await self.bot.get_cog('Verification').verify_adult(author=member, guild=guild)
                except: pass

        #+ Wanting Cultist Verification!
        wanting_cultist = utils.DiscordGet(guild.roles, id=1095724950826004480)
        for member in guild.members:
            if wanting_cultist in member.roles:
                await member.remove_roles(wanting_cultist, reason="Removed wanting cultist role")
                try:
                    await self.bot.get_cog('Verification').verify_cultist(author=member, guild=guild)
                except: pass

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


        #* Levels Leaderboard
        channel = self.bot.get_channel(self.bot.config['channels']['leaderboard'])
        msg = await channel.fetch_message(1095552287298027681)
        msg2 = await channel.fetch_message(1095552293379772466)

        #* Set up the embeds
        embed = Embed(color=randint(1, 0xffffff))
        embed.set_author(name="Top 15 highest levels!")
        embed.set_footer(text="if you ain't on here ya trash, sorry.")
        embed2 = Embed(color=randint(1, 0xffffff))
        embed2.set_author(name="Top 30 highest levels!")
        embed2.set_footer(text="if you ain't on here ya trash, sorry.")


        #* Add in level rankings
        sorted_rank = utils.Levels.sort_levels()
        ranks = sorted_rank[:30]
        users = []
        for i in sorted_rank:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)
        text = []
        text2 = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            if index < 15:
                text.append(f"#{index+1} **{user}** --> Lvl.{floor(rank.level):,}")
            else:
                text2.append(f"#{index+1} **{user}** --> Lvl.{floor(rank.level):,}")

        embed.add_field(name='Level Rank', value='\n'.join(text), inline=True)
        embed2.add_field(name='Level Rank', value='\n'.join(text2), inline=True)

        await msg.edit(content=f"**Those with the Highest Levels!**", embed=embed)
        await msg2.edit(content=f" ", embed=embed2)


        #! Coin Leaderboard
        msg = await channel.fetch_message(1095552313566965760)
        msg2 = await channel.fetch_message(1095552323557806260)

        #* Set up the embeds
        embed = Embed(color=randint(1, 0xffffff))
        embed.set_author(name="Top 10 highest Coins!")
        embed.set_footer(text="Those with the most coins!")
        embed2 = Embed(color=randint(1, 0xffffff))
        embed2.set_author(name="Top 20 highest Coins!")
        embed2.set_footer(text="Those with the most coins!")


        sorted_rank = utils.Currency.sort_coins()
        ranks = sorted_rank[:22]
        users = []
        for i in ranks:
            user = self.bot.get_user(i.user_id)
            if user != None:
                users.append(user)

        text = []
        text2 = []
        for index, (user, rank) in enumerate(zip(users, ranks)):
            if index < 10:
                text.append(f"#{index+1} **{user}** --> {self.bot.config['emotes']['coin']} {floor(rank.coins):,}")
            else:
                text2.append(f"#{index+1} **{user}** --> {self.bot.config['emotes']['coin']} {floor(rank.coins):,}")

        embed.add_field(name='Coin Rank', value='\n'.join(text), inline=True)
        embed2.add_field(name='Coin Rank', value='\n'.join(text2), inline=True)

        await msg.edit(content="**Those with the most coins!**", embed=embed)
        await msg2.edit(content=" ", embed=embed2)

        # + This is the Statistics Channels
        ch = guild.get_channel(self.bot.config['info_channels']['statistics']) #? Stat Channel

        msg1 = await ch.fetch_message(1104655953124655124) #? msg
        msg2 = await ch.fetch_message(1104655958732439552) #? msg
        msg3 = await ch.fetch_message(1104655963006435408) #? msg

        coin_e = self.bot.config['emotes']['coin']
        supporters = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['supporters'])
        nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nitro'])
        t1 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t1'])
        t2 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t2'])
        t3 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t3'])

        #+ Fix the economy!
        sc = utils.Currency.get(550474149332516881)
        total_coins = utils.Currency.get_total_coins()
        difference = self.bot.config['total_coins']-total_coins

        sc.coins += difference
        async with self.bot.database() as db:
            await sc.save(db)

        total_tix = utils.Items.get_total_tickets()
        members = len(set(self.bot.get_all_members()))
        supps = 0
        profit = 0
        nitros = 0
        t1s = 0
        t2s = 0
        t3s = 0
        for user in guild.members:
            if nitro in user.roles:
                nitros += 1
                supps += 1
            if t1 in user.roles:
                profit += 9
                t1s += 1
                supps += 1
            if t2 in user.roles:
                profit += 18
                t2s += 1
                supps += 1
            if t3 in user.roles:
                profit += 27
                t3s += 1
                supps += 1


        embed1=Embed(title=f"**[- Discord Statistics! -]**", 
        description=f"**This show's stats about the Discord Server!**\n\n🎭 Members: **{members:,}**\n💕 Supporters: **{supps:,}**\n<:Ascended:1095161421853098108> Ascended: **{t3s}**\n<:Acolyte:1095161419357499503> Acolyte: **{t2s}**\n<:Initiate:1095161420297011200> Initiate: **{t1s}**\n<:Nitro:1095491689029849189>  Boosters: **{nitros}**", color=0xFF0000)

        embed2=Embed(title=f"**[- Economy Statistics! -]**", 
        description=f"**This show's all the aspects of the Serpent's Economy!**\n\n{coin_e} Total: **{floor(total_coins):,}** Coins\n🐍 Serpent's: **{floor(sc.coins):,}** Coins\n🎟 Current Tickets: **{floor(total_tix):,}**", color=0xFF0000)

        embed3=Embed(title=f"**[- Garden Statistics! -]**", 
        description=f"Coming Soon!", color=0xFFFFFF)


        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)





    @tasks.loop(minutes=60)
    async def one_hour_loop(self):
        """The loop that handles updating things every 60 minutes."""

        #? Check if bot is connected!
        if self.bot.connected == False:
            return

        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild



        #! THE STICKY CODE BLOCK >:O
        bot_usage = guild.get_channel(1028771493179560066) #? bot_usage Channel
        issues = guild.get_channel(1056747603829731338) #? issues Channel
        art = guild.get_channel(1088530067862327376) #? Art Channel
        suggestions = guild.get_channel(1093622505236865045) #? suggestions Channel
        scp_suggestions = guild.get_channel(1056747785749278761) #? SCP suggestions Channel
        emoji_suggestions = guild.get_channel(1109756661331152996) #? Emoji suggestions Channel
        supporter = guild.get_channel(1051738903666769950) #? Supporter Channel
        channels = [bot_usage, issues, scp_suggestions, art, suggestions]
        suggestions = [suggestions, scp_suggestions, emoji_suggestions]
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

                nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nitro'])
                t1 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t1'])
                t2 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t2'])
                t3 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t3'])
                profit = 0
                nitros = 0
                t1s = 0
                t2s = 0
                t3s = 0
                for user in guild.members:
                    if nitro in user.roles:
                        nitros += 1
                    if t1 in user.roles:
                        profit += 9
                        t1s += 1
                    if t2 in user.roles:
                        profit += 18
                        t2s += 1
                    if t3 in user.roles:
                        profit += 27
                        t3s += 1

                #? Check the channels sticky!
                if channel == supporter:
                    embed=Embed(title=f"**[- Supporter Sticky -]**",
                    description=f"**This channel displays any type of support shown to the Serpent's Garden!**\nThank you to everyone who chooses to support the server!\n\n<:Nitro:1095491689029849189> `These are Nitro Boosters` - {nitros} of them!\n<:Initiate:1095161420297011200> `These are 10$ Supporters` - {t1s} of them!\n<:Acolyte:1095161419357499503> `These are 20$ Supporters` - {t2s} of them!\n<:Ascended:1095161421853098108> `These are 30$ Supporters` - {t3s} of them!\n\n**For Serpent's Garden to be self sustaining**\nWe'd need to reach this goal: `{profit}$ / 200$` (Keep in mind Discord takes a cut.)\n\n*But don't worry!  There is no plans of taking Serpent's Garden down for not reaching goal anytime soon! <3*", color=randint(1, 0xffffff))
                if channel == bot_usage:
                    embed=Embed(title=f"**[- Bot Usage Sticky -]**",
                    description=f"**This channel is only for using bot commands!**\nthe Serpent bot has the `/` prefix for regular commands.\nThe Serpent's Music commands use the prefix `!` and both have a help command!", color=randint(1, 0xffffff))
                if channel == art:
                    embed=Embed(title=f"**[- Art Sticky -]**",
                    description=f"**This channel is for posting art created by the community!**\n__No AI art, Memes or anything you didn't create is allowed__\n\n*Please keep furry art in the furry channels however!*", color=randint(1, 0xffffff))
                if channel == issues:
                    embed=Embed(title=f"**[- Issues Sticky -]**",
                    description=f"**This channel is for pinging staff about issues happening the SCP servers!**\n*Please follow these guidelines before you ping!*\n\n**<@&891793700932431942>** - Ping for Major bugs or anything if you think its important enough.\n**<@&1068389027222405221>** - Ping for anything SCP Server related.\n**<@&1068389119195107378>** - Ping for anything Discord related.", color=randint(1, 0xffffff))
                for channel in suggestions:
                    embed=Embed(title=f"**[- Suggestion Stickys! -]**",
                    description=f"**Please do not just hold conversations or make replies here!**\n\nYou can create a thread to reply to suggestions!", color=randint(1, 0xffffff))
                try:
                    await msg.edit(content=f" ", embed=embed)
                except: 
                    print(f'Couldnt edit sticky for {channel}')





    @ten_sec_loop.before_loop
    async def before_three_sec_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""

        await self.bot.wait_until_ready()

    @one_min_loop.before_loop
    async def before_one_min_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""

        await self.bot.wait_until_ready()


    @one_hour_loop.before_loop
    async def before_one_hour_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""

        await self.bot.wait_until_ready()





def setup(bot):
    x = Loops(bot)
    bot.add_cog(x)
