# Discord
from discord.ext.commands import command, Cog, Greedy
from discord import Member, Message, User, TextChannel

# Additions
from random import randint
from datetime import datetime as dt, timedelta
from more_itertools import unique_everseen
from re import search
from asyncio import sleep
from re import compile

import utils


class Chat_Moderation(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_posted = dt(year=2000, month=1, day=1)  # Some time in the definite past 
        self.valid_uri = compile(r"(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")



    async def bot_warn(self, channel, user:Member, reason:str):
        guild = self.bot.get_guild(self.bot.config['guilds']['RaziRealmID']) #? Guild

        if reason == "Spamming":
            m = await channel.send(embed=utils.WarningEmbed(user=user, title=f"{user} was warned for spamming.", guild=channel.guild))

        if reason == "Language":
            m = await channel.send(embed=utils.WarningEmbed(user=user, title=f"{user} was warned for bad word usage.", guild=channel.guild))
        await sleep(3)
        await m.delete()



    @Cog.listener('on_message')
    async def chat_moderation(self, message:Message):
        # BETTER NOT BE A DM!
        if message.guild == None:
            return
        # Bots don't do things!
        if message.author.bot: 
            return

        # Define some variables
        user = message.author
        contents = message.content.split()
        total_words = len(message.content.split())
        unique_words = len(list(unique_everseen(message.content.split(), str.lower)))
        total_letters = len(list(message.content))
        chat_filter = ([
            "nigger",
            "nigga",
            "niggr",
            "ngger",
            "nifger",
            "Niggerz",
            "nlgger",
            "niqqer",
            "niggas",
            "ngger",
            "Nigg",
            "nggr",
            "ngger",
            "nigga",
            "nig.ger",
            "nig",
            "gook"
        ])

        #! Keep it from ghosting...
        await sleep(1)

        # # Spamming
        # if total_words > 4:
        #     if total_words*0.35 > unique_words:
        #         await message.delete()
        #         await self.bot_warn(channel=message.channel, user=user, reason="Spamming")
        #         return

        #     elif total_letters/0.75 < total_words:
        #         await message.delete()
        #         await self.bot_warn(channel=message.channel, user=user, reason="Spamming")
        #         return

        # Censors all dem baddies!
        for word in contents:
            if word.lower() in chat_filter:
                await message.delete()
                await self.bot_warn(channel=message.channel, user=user, reason="Language")
                return


    # @Cog.listener('on_message')
    # async def image_handler_listener(self, message):
    #     '''Looks for attachments on messages sent in general'''
    #     # Check for general
    #     if message.channel.id != self.bot.config['channels']['general']:
    #         return
    #     # Staff bypass
    #     if [i for i in message.author.roles if i.id == self.bot.config['roles']['staff']]:
    #         return
    #     # Check for links
    #     if message.content.strip().lower() != self.valid_uri.match(message.content.split(" ")[0].split("\n")[0]): return
    #     # Check for attachments
    #     if message.attachments == None:
    #         return
    #     # Check counter
    #     if dt.utcnow() - timedelta(minutes=3) < self.last_posted:
    #         await message.delete()
    #         m = await message.channel.send(embed=utils.WarningEmbed(user=message.author, title="Images are only allowed in general every 3 minutes."))
    #     else:
    #         self.last_posted = message.created_at



def setup(bot):
    x = Chat_Moderation(bot)
    bot.add_cog(x)
