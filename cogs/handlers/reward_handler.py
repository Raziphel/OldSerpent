# Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter
from discord import Member, Message, User, TextChannel, Role, RawReactionActionEvent, Embed
# Additions
from datetime import datetime as dt, timedelta
from asyncio import iscoroutine, gather, sleep
from math import floor 
from random import choice, randint

import utils


class Reward_Handler(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bunny_messages = []
        self.silver_messages = []
        self.gold_messages = []
        self.good_messages = []
        self.evil_messages = []

    @property  #! The currency logs
    def currency_log(self):
        return self.bot.get_channel(self.bot.config['channels']['currency_log'])

    @Cog.listener('on_message')
    async def reward_gen(self, message):
        '''Message Reward Generation'''

        #? BETTER NOT BE A DM
        if message.guild == None:
            return
        #? Disables Bots
        if message.author.bot:
            return
        #? Check if bot is connected!
        if self.bot.connected == False:
            return
        if message.channel.history == None:
            return

        #! Define some variables
        user = message.author
        messages = await message.channel.history(limit=8).flatten()

        #! Give them some rewards!
        chance = randint(1, 35000)
        if chance <= 5:
            message = choice(messages)
            await message.add_reaction(self.bot.config['emotes']['evilcoin'])
            self.evil_messages.append(message.id)
        elif chance <= 150:
            message = choice(messages)
            await message.add_reaction(self.bot.config['emotes']['goodcoin'])
            self.good_messages.append(message.id)
        elif chance <= 500:
            message = choice(messages)
            await message.add_reaction(self.bot.config['emotes']['goldcoin'])
            self.gold_messages.append(message.id)




    @Cog.listener('on_raw_reaction_add')
    async def item_reaction_handler(self, payload:RawReactionActionEvent):
        '''Handles reactions with the items'''

        #? Check if bot is connected!
        if self.bot.connected == False:
            return


        #? BETTER NOT BE A DM
        guild = self.bot.get_guild(payload.guild_id)
        user = self.bot.get_user(payload.user_id)
        if guild == None:
            return

        #? Check not a bot
        if user.bot:
            return

        #! Define Varibles
        c = utils.Currency.get(user.id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        msg = None


        #! Define Emojis
        gold_e = self.bot.config['emotes']['goldcoin']
        good_e =self.bot.config['emotes']['goodcoin']
        evil_e = self.bot.config['emotes']['evilcoin']

        #! Get the correct item
        if str(payload.emoji) == gold_e:
            if message.id in self.gold_messages:
                self.gold_messages.remove(message.id)
                await message.clear_reactions()
                gold_coins = choice([25, 15, 5])
                c.gold_coins += gold_coins
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{gold_coins} {gold_e}x**", footer=f"", guild=guild))
                try: await self.currency_log.send(embed=utils.LogEmbed(type="special", title=f"{user} found a reward!", desc=f"{user} found **{gold_coins} {gold_e}x**", guild=guild))
                except: pass

        elif str(payload.emoji) == good_e:
            if message.id in self.good_messages:
                self.good_messages.remove(message.id)
                await message.clear_reactions()
                good_coins = choice([5, 10, 15])
                c.good_coins += good_coins
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{good_coins} {good_e}x**", footer=f"", guild=guild))
                try: await self.currency_log.send(embed=utils.LogEmbed(type="special", title=f"{user} found a reward!", desc=f"{user} found **{good_coins} {good_e}x**", guild=guild))
                except: pass

        elif str(payload.emoji) == evil_e:
            if message.id in self.evil_messages:
                self.evil_messages.remove(message.id)
                await message.clear_reactions()
                evil_coins = choice([1, 2, 3])
                c.evil_coins += evil_coins
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{evil_coins} {evil_e}x**", footer=f"", guild=guild))
                try: await self.currency_log.send(embed=utils.LogEmbed(type="special", title=f"{user} found a reward!", desc=f"{user} found **{evil_coins} {evil_e}x**", guild=guild))
                except: pass

        else: 
            return

        #! Save it to database
        async with self.bot.database() as db:
            await c.save(db)

        if msg != None:
            await sleep(3)
            await msg.delete()
        else: 
            return


def setup(bot):
    x = Reward_Handler(bot)
    bot.add_cog(x)