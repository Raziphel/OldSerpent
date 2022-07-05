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
        self.ruby_messages = []
        self.sapphire_messages = []
        self.emerald_messages = []
        self.diamond_messages = []
        self.amethyst_messages = []
        self.crimson_messages = []



    @property  #! The currency logs
    def currency_log(self):
        return self.bot.get_channel(self.bot.config['channels']['currency_log']) #?Currency log channel


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
        messages = await message.channel.history(limit=10).flatten()

        #! Give them some rewards!
        try:
            chance = randint(1, 100000)
            if chance <= 3:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emotes']['crimson'])
                self.crimson_messages.append(message.id)
            elif chance <= 200:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emotes']['amethyst'])
                self.amethyst_messages.append(message.id)
            elif chance <= 500:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emotes']['sapphire'])
                self.sapphire_messages.append(message.id)
            elif chance <= 1000:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emotes']['ruby'])
                self.ruby_messages.append(message.id)
            elif chance <= 1700:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emotes']['diamond'])
                self.diamond_messages.append(message.id)
            elif chance <= 3000:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emotes']['emerald'])
                self.emerald_messages.append(message.id)
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


        #! Get the correct item
        if str(payload.emoji) == self.bot.config['emotes']['crimson']:
            if message.id in self.crimson_messages:
                self.crimson_messages.remove(message.id)
                await message.clear_reactions()
                crimson = 1
                c.crimson += crimson
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{crimson} {self.bot.config['emotes']['crimson']}x**", footer=f""))
                try: await self.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"{user} found Crimson!", desc=f"{user} found **{round(crimson)} {self.bot.config['emotes']['crimson']}x**"))
                except: pass



        elif str(payload.emoji) == self.bot.config['emotes']['amethyst']:
            if message.id in self.amethyst_messages:
                self.amethyst_messages.remove(message.id)
                await message.clear_reactions()
                amethyst = choice([1, 2, 3])
                c.amethyst += amethyst
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{round(amethyst)} {self.bot.config['emotes']['amethyst']}x**", footer=f""))
                try: await self.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"{user} found a Amethyst!", desc=f"{user} found **{round(amethyst)} {self.bot.config['emotes']['amethyst']}x**"))
                except: pass



        elif str(payload.emoji) == self.bot.config['emotes']['ruby']:
            if message.id in self.ruby_messages:
                self.ruby_messages.remove(message.id)
                await message.clear_reactions()
                ruby = choice([4, 5, 6])
                c.ruby += ruby
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{round(ruby)} {self.bot.config['emotes']['ruby']}x**", footer=f""))
                try: await self.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"{user} found a Ruby!", desc=f"{user} found **{round(ruby)} {self.bot.config['emotes']['ruby']}x**"))
                except: pass



        elif str(payload.emoji) == self.bot.config['emotes']['sapphire']:
            if message.id in self.sapphire_messages:
                self.sapphire_messages.remove(message.id)
                await message.clear_reactions()
                sapphire = choice([7, 9, 11])
                c.sapphire += sapphire
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{round(sapphire)} {self.bot.config['emotes']['sapphire']}x**", footer=f""))
                try: await self.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"{user} found a Sapphire!", desc=f"{user} found **{round(sapphire)} {self.bot.config['emotes']['sapphire']}x**"))
                except: pass



        elif str(payload.emoji) == self.bot.config['emotes']['diamond']:
            if message.id in self.diamond_messages:
                self.diamond_messages.remove(message.id)
                await message.clear_reactions()
                diamond = choice([15, 20, 25])
                c.diamond += diamond
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{round(diamond)} {self.bot.config['emotes']['diamond']}x**", footer=f""))
                try: await self.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"{user} found a Diamond!", desc=f"{user} found **{round(diamond)} {self.bot.config['emotes']['diamond']}x**"))
                except: pass



        elif str(payload.emoji) == self.bot.config['emotes']['emerald']:
            if message.id in self.emerald_messages:
                self.emerald_messages.remove(message.id)
                await message.clear_reactions()
                emerald = choice([25, 40, 50])
                c.emerald += emerald
                msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{round(emerald)} {self.bot.config['emotes']['emerald']}x**", footer=f""))
                try: await self.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"{user} found a Emerald!", desc=f"{user} found **{round(emerald)} {self.bot.config['emotes']['emerald']}x**"))
                except: pass




        #! Save it to database
        async with self.bot.database() as db:
            await c.save(db)

        if msg != None:
            await sleep(3)
            await msg.delete()
        else: 
            return


def setup(bot):
    x = Message_Rewards(bot)
    bot.add_cog(x)