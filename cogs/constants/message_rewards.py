# Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter
from discord import Member, Message, User, TextChannel, Role, RawReactionActionEvent, Embed
# Additions
from datetime import datetime as dt, timedelta
from asyncio import iscoroutine, gather, sleep
from math import floor 
from random import choice, randint

import utils


class Message_Rewards(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bunny_messages = []
        self.silver_messages = []
        self.gold_messages = []
        self.emerald_messages = []
        self.diamond_messages = []



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

        #! Define some variables
        user = message.author
        messages = await message.channel.history(limit=8).flatten()

        #! Give them some rewards!
        try:
            chance = randint(1, 70000)
            if chance <= 5:
                message = choice(messages)
                await message.add_reaction("<:Diamond:766123219609976832>")
                self.diamond_messages.append(message.id)
            elif chance <= 150:
                message = choice(messages)
                await message.add_reaction("<:Emerald:766123219731611668>")
                self.emerald_messages.append(message.id)
            elif chance <= 500:
                message = choice(messages)
                await message.add_reaction("<:GoldIngot:766123219827949596>")
                self.gold_messages.append(message.id)
            elif chance <= 1000:
                message = choice(messages)
                await message.add_reaction("<:Silver:766123219761233961>")
                self.silver_messages.append(message.id)
        except Exception as e:
            print(f'A reward failed to spawn :: {e}')




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

        log = await utils.ChannelFunction.get_log_channel(guild=guild, log="currency")

        #! Define Emojis
        bunny_e = "<a:Bunny:703136644366336000>"
        diamond_e = "<:Diamond:766123219609976832>"
        emerald_e = "<:Emerald:766123219731611668>"
        silver_e = "<:Silver:766123219761233961>"
        gold_e = "<:GoldIngot:766123219827949596>"

        #! Get the correct item
        if str(payload.emoji) == silver_e:
            if message.id in self.silver_messages:
                self.silver_messages.remove(message.id)
                await message.clear_reactions()
                silver = choice([25, 50, 75])
                c.silver += silver
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{silver} {silver_e}x**", footer=f"", guild=guild))
                try: await log.send(embed=utils.LogEmbed(type="special", title=f"{user} found a reward!", desc=f"{user} found **{silver} {silver_e}x**", guild=guild))
                except: pass

        elif str(payload.emoji) == gold_e:
            if message.id in self.gold_messages:
                self.gold_messages.remove(message.id)
                await message.clear_reactions()
                gold = choice([25, 15, 5])
                c.gold += gold
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{gold} {gold_e}x**", footer=f"", guild=guild))
                try: await log.send(embed=utils.LogEmbed(type="special", title=f"{user} found a reward!", desc=f"{user} found **{gold} {gold_e}x**", guild=guild))
                except: pass

        elif str(payload.emoji) == emerald_e:
            if message.id in self.emerald_messages:
                self.emerald_messages.remove(message.id)
                await message.clear_reactions()
                emerald = choice([5, 10, 15])
                c.emerald += emerald
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{emerald} {emerald_e}x**", footer=f"", guild=guild))
                try: await log.send(embed=utils.LogEmbed(type="special", title=f"{user} found a reward!", desc=f"{user} found **{emerald} {emerald_e}x**", guild=guild))
                except: pass

        elif str(payload.emoji) == diamond_e:
            if message.id in self.diamond_messages:
                self.diamond_messages.remove(message.id)
                await message.clear_reactions()
                diamond = choice([1, 2, 3])
                c.diamond += diamond
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{diamond} {diamond_e}x**", footer=f"", guild=guild))
                try: await log.send(embed=utils.LogEmbed(type="special", title=f"{user} found a reward!", desc=f"{user} found **{diamond} {diamond_e}x**", guild=guild))
                except: pass

        else: 
            return

        #! Save it to database
        async with self.bot.database() as db:
            await c.save(db)

        if msg != None:
            await sleep(3)
            await msg.delete()
            await utils.GemFunction.update_gems(user=user)
        else: 
            return


def setup(bot):
    x = Message_Rewards(bot)
    bot.add_cog(x)