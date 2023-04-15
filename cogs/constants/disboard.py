import re
from datetime import datetime, timedelta

from discord.ext.commands import Cog
from discord.ext import tasks

from utils.exceptions import Misconfigured


class Disboard(Cog):
    DISBOARD_BOT_ID = 302050872383242240

    def __init__(self, bot):
        self.bot = bot
        self.last_bump = datetime.utcnow()
        self.open_window.start()
        self.open = False

    def cog_unload(self):
        self.open_window.cancel()
        self.ping_users.cancel()

    def role(self):
        return self.bot.config('bump', 'disboard_role')

    def channel(self):
        return self.bot.config('bump', 'disboard_channel')

    @tasks.loop(seconds=60.0)
    async def open_window(self):
        now = datetime.utcnow()
        if self.last_bump + timedelta(hours=2) <= now:
            if not self.open:
                self.open = True
                if not self.ping_users.is_running():
                    self.ping_users.start()
                else:
                    self.ping_users.restart()

    @tasks.loop(minutes=10.0)
    async def ping_users(self):
        role = self.role()
        ch_id = self.channel()
        ch = self.bot.get_channel(ch_id)
        if not ch:
            raise Misconfigured('bumping', 'discordme', 'channel (TextChannel)')
        if self.open:
            await ch.send(
                f"<@&{role}> It is time to bump !!"
            )
        else:
            self.ping_users.cancel()

    @commands.Cog.listener()
    async def on_message(self, message):
        ch = message.channel
        content = message.content
        if content.lower() != "!d bump":
            return
        elif ch.id != self.channel():
            return
        else:
            def check(m):
                return m.author.id == self.DISBOARD_BOT_ID
        msg = await self.bot.wait_for('message', check=check)
        created_at = msg.created_at
        if not (embeds := msg.embeds):
            return
        em = embeds[0]
        desc = em.description
        if "Bump done" in desc:
            self.last_bump = created_at
            await ch.send(
                f"Bumping are we? I will remind the Bump Squad to bump again in 2 hours from now. "
            )
        elif "Please wait" in desc:
            if match := re.search(r'another (\d+) minute', desc):
                minutes = int(match.group(1))
                self.last_bump = created_at - timedelta(minutes=120 - minutes)
                await ch.send(
                    f"{minutes} minutes left."
                )
        self.open = False

    @commands.Cog.listener()
    async def on_ready(self):
        ch = self.bot.get_channel(self.channel())
        if not ch:
            raise Misconfigured('bumping', 'disboard', 'channel (TextChannel)')
        async for msg in ch.history():
            author = msg.author
            created_at = msg.created_at
            if author.id != self.DISBOARD_BOT_ID:
                continue
            elif not (embeds := msg.embeds):
                continue
            em = embeds[0]
            desc = em.description
            if "Bump done" in desc:
                self.last_bump = created_at
                return
            elif "Please wait" in desc:
                if match := re.search(r'another (\d+) minute', desc):
                    minutes = int(match.group(1))
                    last_bump = created_at - timedelta(minutes=120 - minutes)
                    self.last_bump = last_bump
                    if minutes > 0:
                        return
                    else:
                        # It's bump time but we already have the loops to handle that so do nothing at this point.
                        return
                else:
                    continue  # idk how tf this would happen butt ye
            else:
                continue  # In the case of disboard maybe returning an error on this specific msg


def setup(bot):
    x = Disboard(bot)
    bot.add_cog(x)
