# Discord
from discord.ext.commands import Cog
from discord import RawReactionActionEvent, Embed

import utils

# Additions
from more_itertools import unique_everseen
from datetime import datetime as dt, timedelta
from asyncio import sleep
from math import floor

from re import search

class Listeners(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_image = dt(year=2000, month=1, day=1)  # Some time in the definite past 
        self.reminded = []
        self.spotifyReg = r"^https:\/\/open\.spotify\.com.*"



    @Cog.listener('on_message')
    async def music_handler_listener(self, message):
        '''Looks for spotify music!'''

        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(1138195661288914995) #? music Channel

        #? Check for music channel
        if message.channel.id == ch.id:
            return

        if search(self.spotifyReg, message.content):
            await ch.send(f"**{message.author.name} Posted a song in <#{message.channel.id}>**\n {message.content}")







    @Cog.listener('on_message')
    async def Monthly_Reminder(self, message):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        day = utils.Daily.get(message.author.id)

        nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nitro'])
        t1 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t1'])
        t2 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t2'])
        t3 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t3'])
        supporterroles = [nitro, t1, t2, t3]

        try:
            for role in message.author.roles:
                if role in supporterroles:
                    if (day.monthly + timedelta(days=29)) <= dt.utcnow():
                        if message.author.id not in self.reminded:
                            await message.author.send(embed=utils.DefaultEmbed(title="Monthly Reminder!", desc="You can now claim your monthly reward!", footer=" "))
                            self.reminded.append(message.author.id)
        except: pass




    # @Cog.listener('on_message')
    # async def stream_ping(self, message):
    #     '''Ping when a streamer pings!'''
    #     if message.channel.id == 1051323487287005264:
    #         if message.author.id != 550474149332516881:
    #             await message.channel.send(f"<@&1070576949837180939>")


    @Cog.listener('on_reaction_add')
    async def remove_bad_reactions(self, reaction, user):
        if self.bot.get_user(user.id).bot:
            return

        #* Get the coin emojis
        coin = self.bot.config['emotes']['coin']
        bunny = self.bot.config['emotes']['bunny']

        disallowed_emotes = [coin, bunny, "✨", "🎟"]

        if str(reaction.emoji) in disallowed_emotes:
            #+ Remove the reaction
            await reaction.remove(user)


    # @Cog.listener('on_message')
    # async def on_messages_razi(self, message):
    #     '''tell people off'''

    #     #! Stop bots at this point...
    #     if message.author.bot: 
    #         return

    #     #+ Keep track of peoples message count!
    #     unique_words = list(unique_everseen(message.content.split(), str.lower))
    #     razis = ['Razi', 'razi', '@Razi', '<@159516156728836097>', 'razi.', 'Razi.', 'razi!', 'Razi!', 'RAZI']
    #     for razi in razis:
    #         if razi in unique_words:
    #             msg = await message.channel.send('Show respect to her name.')
    #             # await sleep(4)
    #             # await msg.delete()





    @Cog.listener('on_message')
    async def on_messages(self, message):
        '''Adds votes reactions!'''

        #+ Keep track of peoples message count!
        tr = utils.Tracking.get(message.author.id)
        tr.messages += 1
        async with self.bot.database() as db:
            await tr.save(db)



        #+ Check for Suggestion channels
        if message.channel.id in [1093622505236865045, 1056747785749278761, 1109756661331152996, 1159044488208056341, 1180049869549871197]: #? Suggestions
            if message.author.bot:
                return
            await message.add_reaction("<:UpVote:1041606985080119377>")
            await message.add_reaction("<:DownVote:1041606970492342282>")
        # if message.channel.id in [1051033412456165396]: #? 1 word only
        #     total_words = len(message.content.split())
        #     if total_words > 1 or list(message.content) in ["=", "-", "_", "~", "`", "."]:
        #         await message.delete()
        #         await message.channel.send(embed=utils.DefaultEmbed(title="1 Word Only!", desc="If it wasn't obvious you can only send 1 word."), delete_after=5)



    # @Cog.listener()
    # async def on_member_update(self, before, after):
    #     guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
    #     if before.premium_since is None and after.premium_since is not None:
    #         c = utils.Currency(before.id)
    #         coin = self.bot.config['emotes']['coin']
    #         total_coins = 0
    #         try:
    #             await user.send(embed=utils.SpecialEmbed(title="- Nitro Rewards -", desc=f"A reward for being a nitro booster!\n\n**+5,000 {coin}**", footer=f"You can expect this reward every 30 days!"))
    #         except: pass
    #         c.coins += 5000
    #         total_coins += 5000
    #         for user in guild.members:
    #             nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nitro'])
    #             if nitro in user.roles:
    #                 c = utils.Currency(user.id)
    #                 try:
    #                     await user.send(embed=utils.SpecialEmbed(title="- Nitro Rewards -", desc=f"A smaller reward becuase someone nitro boosted!\n\n**+1,000 {coin}**", footer=f"You can expect this reward every time someone boosts!"))
    #                 except: pass
    #                 c.coins += 1000
    #                 total_coins += 1000
    #                 async with self.bot.database() as db:
    #                     await c.save(db)

    #         supporters = self.bot.get_channel(self.bot.config['channels']['supporters'])
    #         await supporters.send(embed=utils.SpecialEmbed(desc=f"*All nitro boosters recieved a reward!*\n**Total Coins:** {total_coins:,} {coin}", footer=f" "))



def setup(bot):
    x = Listeners(bot)
    bot.add_cog(x)
