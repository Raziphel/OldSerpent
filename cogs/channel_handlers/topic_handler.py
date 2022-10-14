
#* Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter
from discord import Member, Message, User, TextChannel, Role, RawReactionActionEvent, Embed
from discord.ext import tasks
import utils
#* Additions
from asyncio import iscoroutine, gather, sleep
from traceback import format_exc
from math import floor
from random import randint
from datetime import datetime as dt, timedelta

import utils

class topic_handler(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.five_min_loop.start()




    @tasks.loop(minutes=1)
    async def five_min_loop(self):
        """The loop that handles updating things every 5 minutes."""

        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        for channel in guild.text_channels:
            
            
            await channel.edit(topic=f"")
            await sleep(3)






    @five_min_loop.before_loop
    async def before_five_min_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""
        
        await self.bot.wait_until_ready()




def setup(bot):
    x = topic_handler(bot)
    bot.add_cog(x)