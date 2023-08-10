import asyncio
from datetime import timedelta
import discord
from discord.ext import commands


DISCORDME_BUMP_TEXT = """
<@&1130827884324458607> Please bump the server on https://Discord.me/Dashboard  
"""

DISBOARD_BUMP_TEXT = """
<@&1130827884324458607> Please run `/bump` with the Disboard bot.
"""

class BumpHandler(commands.Cog):

    BUMP_CHANNEL_ID = 1020831172181372958  # TODO move to config
    DISCORDME_USER_ID = 1020831331736887406  # TODO move to config

    DISCORDME_TIMEOUT = timedelta(hours=6)  # TODO move to config
    DISCORDME_GRACE_PERIOD = timedelta(minutes=5)  # TODO move to config



    DISBOARD_USER_ID = 302050872383242240  # TODO move to config

    DISBOARD_TIMEOUT = timedelta(hours=2)  # TODO move to config
    DISBOARD_GRACE_PERIOD = timedelta(minutes=5)  # TODO move to config


    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.notify_task = None
        self.notify_task2 = None


    async def bump_timer(self):
        """
        Wait for N minutes, send a message in the specified channel.
        """

        await asyncio.sleep(
            (self.DISCORDME_TIMEOUT + self.DISCORDME_GRACE_PERIOD)
            .total_seconds()
        )
        channel = self.bot.get_partial_messageable(self.BUMP_CHANNEL_ID)
        await channel.send(BUMP_TEXT)


    @commands.Cog.listener()
    async def on_ready(self):
        if self.notify_task is not None:
            self.notify_task = asyncio.create_task(self.bump_timer())

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Listens for the "this guild has been bumped" message, and
        queues up a reminder to go in 6 hours.
        """

        # Make sure we're in the right place
        if message.guild is None:
            return
        if message.author.id != self.DISCORDME_USER_ID:
            return

        # Check the message sent
        if "on Discord Me." not in message.content:
            return

        # Alright, reset/start timer
        if self.notify_task is not None:
            self.notify_task.cancel()
        self.notify_task = asyncio.create_task(self.bump_timer())





    async def bump_timer2(self):
        """
        Wait for N minutes, send a message in the specified channel.
        """

        await asyncio.sleep(
            (self.DISBOARD_TIMEOUT + self.DISBOARD_GRACE_PERIOD)
            .total_seconds()
        )
        channel = self.bot.get_partial_messageable(self.BUMP_CHANNEL_ID)
        await channel.send(BUMP_TEXT)


    @commands.Cog.listener()
    async def on_ready(self):
        if self.notify_task2 is not None:
            self.notify_task2 = asyncio.create_task(self.bump_timer2())

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Listens for the "this guild has been bumped" message, and
        queues up a reminder to go in 2 hours.
        """

        # Make sure we're in the right place
        if message.guild is None:
            return

        # Check the message sent
        if not message.embeds:
            return
        embed = message.embeds[0]
        if not isinstance(embed.description, str):
            return
        if "bump done!" not in embed.description.casefold():
            return


        # Alright, reset/start timer
        if self.notify_task2 is not None:
            self.notify_task2.cancel()
        self.notify_task2 = asyncio.create_task(self.bump_timer2())






def setup(bot: commands.Bot):
    x = BumpHandler(bot)
    bot.add_cog(x)
