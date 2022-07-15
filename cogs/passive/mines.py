# Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter
from discord import Member, Message, User, TextChannel, Role, RawReactionActionEvent, Embed
# Additions
from datetime import datetime as dt, timedelta
from discord.ext import tasks
from asyncio import iscoroutine, gather, sleep
from math import floor 
from random import choice, randint

import utils


class Mines(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_reward = dt(year=2000, month=1, day=1)
        self.mines_loop.start()

    @tasks.loop(minutes=1)
    async def mines_loop(self):
        """The loop that handles the leaderboard updating"""

        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['mines']) #? Mines Channel
        m = utils.Mines.get(self.bot.config['channels']['mines'])
        msg = await ch.fetch_message(m.last_msg)

        if dt.utcnow() - timedelta(minutes=5) < self.last_reward:
            await msg.edit(embed=utils.SpecialEmbed(color=0xdc143c, title=f'Reward has already been claimed!', desc=f'Last Miner: <@{m.last_user}>\nRecieved: {m.last_reward_type} {m.last_reward_amount}x'))
        else:
            await msg.edit(embed=utils.SpecialEmbed(color=0xdc143c, title=f'Click the ⛏ to mine for gems!', desc=f'Last Miner: <@{m.last_user}>\nRecieved: {m.last_reward_type} {m.last_reward_amount}x'))
            await msg.add_reaction("⛏")



    @mines_loop.before_loop
    async def before_mines_update_loop(self):
        """Waits until the cache loads up before running the leaderboard loop"""
        
        await self.bot.wait_until_ready()



    @Cog.listener('on_raw_reaction_add')
    async def mining(self, payload:RawReactionActionEvent):
        """Reaction role add handler"""

        # Validate channel
        if payload.channel_id != self.bot.config['channels']['mines']:
            return

        # Not bot
        if self.bot.get_user(payload.user_id).bot:
            return

        # See what the emoji is
        if payload.emoji.is_unicode_emoji():
            emoji = payload.emoji.name
        else:
            emoji = payload.emoji.id

        # Work out out cached items
        channel = self.bot.get_channel(payload.channel_id)
        guild = channel.guild
        member = guild.get_member(payload.user_id)
        m = utils.Mines.get(self.bot.config['channels']['mines'])
        c = utils.Currency.get(member.id)
        msg = await channel.fetch_message(m.last_msg)

        # Get the reaction
        if emoji == "⛏":
            if dt.utcnow() - timedelta(minutes=5) > self.last_reward:
                await msg.clear_reactions()
                type_ = choice(['<:Silver:994737895707525181>', '<:Gold:994737893014773790>', '<:Emerald:994737891735511050>', '<:Diamond:994737890582069278>'])
                amount = choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60])
                m.last_reward_type = type_
                m.last_reward_amount = amount
                msg = await channel.send(embed=utils.SpecialEmbed(color=0xdc143c, title=f'You managed to do some mining!!', desc=f'You have recieved: {m.last_reward_type} {m.last_reward_amount}x'))
                m.last_msg = msg.id

                if type_ == "<:Silver:994737895707525181>":
                    c.silver += amount
                elif type_ == "<:Gold:994737893014773790>":
                    c.gold += amount
                elif type_ == "<:Emerald:994737891735511050>":
                    c.emerald += amount
                elif type_ == "<:Diamond:994737890582069278>":
                    c.diamond += amount

                async with self.bot.database() as db:
                    await m.save(db)
                    await c.save(db)
                await utils.GemFunction.update_gems(user=member)


        # Check to see total reactions on the message
        message = await channel.fetch_message(payload.message_id)
        emoji = [i.emoji for i in message.reactions]
        if sum([i.count for i in message.reactions]) > 200:
            await message.clear_reactions()
        for e in emoji:
            await message.add_reaction(e)


    @utils.is_dev()
    @command(hidden=True)
    async def setmsg(self, ctx):
        m = utils.Mines.get(ctx.channel.id)
        msg = await ctx.send(f'Yes sir.') 
        m.last_msg = msg.id
        async with self.bot.database() as db:
            await m.save(db)

def setup(bot):
    x = Mines(bot)
    bot.add_cog(x)