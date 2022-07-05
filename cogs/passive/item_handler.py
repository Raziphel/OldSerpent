# Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter
from discord import Member, Message, User, Game, Embed
from discord import Member, Message, User, TextChannel, Role, RawReactionActionEvent, Embed
# Additions
from datetime import datetime as dt, timedelta
from asyncio import iscoroutine, gather, sleep
from math import floor 
from random import choice, randint

import utils

class item_handler(Cog):
    def __init__(self, bot):
        self.bot = bot
    #     self.bunny_messages = []
    #     self.coin_messages = []

    # @Cog.listener('on_message')
    # async def random_coin_gen(self, message):
    #     '''Random Coin Generation'''

    #     # BETTER NOT BE A DM
    #     if message.guild == None:
    #         return
    #     # Disables Bots
    #     if message.author.bot:
    #         return

    #     # Define some variables
    #     user = message.author
    #     messages = await message.channel.history(limit=10).flatten()

    #     #! Give them some coins!
    #     chance = randint(1, 100)
    #     if chance <= 1:
    #         message = choice(messages)
    #         await message.add_reaction("<:RaziCoin:690014230413443223>")
    #         self.coin_messages.append(message.id)




    # @Cog.listener('on_message')
    # async def random_evil_coins(self, message):
    #     '''Random Evil Coin Generation'''

    #     # BETTER NOT BE A DM
    #     if message.guild == None:
    #         return
    #     # Disables Bots
    #     if message.author.bot:
    #         return

    #     # Define some variables
    #     user = message.author
    #     messages = await message.channel.history(limit=10).flatten()

    #     #! Give them some evil coins!
    #     chance = randint(1, 7000)
    #     if chance <= 1:
    #         message = choice(messages)
    #         await message.add_reaction("<:EvilRaziCoin:702950117514281072>")
    #         self.coin_messages.append(message.id)




    # @Cog.listener('on_message')
    # async def bunny_gen(self, message):
    #     '''Bunny Generation'''

    #     # BETTER NOT BE A DM
    #     if message.guild == None:
    #         return
    #     # Disables Bots
    #     if message.author.bot:
    #         return

    #     # Define some variables
    #     user = message.author
    #     msg = None
    #     items = utils.Items.get(message.author.id)

    #     #! Give them the bunny
    #     rl = items.rabbit_luck
    #     chance = randint(1, 12000)
    #     if chance <= rl:
    #         messages = await message.channel.history(limit=12).flatten()
    #         for message in messages:
    #             chance = choice([1, 2, 3])
    #             if chance == 3:
    #                 await message.add_reaction("<a:Bunny:703136644366336000>")
    #                 self.bunny_messages.append(message.id)




    # @Cog.listener('on_raw_reaction_add')
    # async def item_reaction_handler(self, payload:RawReactionActionEvent):
    #     '''Handles reactions with the items'''
    #     if self.bot.get_user(payload.user_id).bot:
    #         return

    #     # Define varibles
    #     guild = self.bot.get_guild(payload.guild_id)
    #     channel = guild.get_channel(payload.channel_id)
    #     message = await channel.fetch_message(payload.message_id)
    #     user = guild.get_member(payload.user_id)
    #     c = utils.Currency.get(user.id)
    #     msg = None

    #     coins_e = "<:RaziCoin:690014230413443223>"
    #     evil_coins_e = "<:EvilRaziCoin:702950117514281072>"
    #     bunny_e = "<a:Bunny:703136644366336000>"


    #     # Get the correct item
    #     if str(payload.emoji) == coins_e:
    #         if message.id in self.coin_messages:
    #             self.coin_messages.remove(message.id)
    #             await message.clear_reactions()
    #             coins = choice([50, 60, 50])
    #             c.coins += coins
    #             msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{coins} coins! {coins_e}** ~"))
    #             # Save it to database
    #             async with self.bot.database() as db:
    #                 await c.save(db)

    #     elif str(payload.emoji) == evil_coins_e:
    #         if message.id in self.coin_messages:
    #             self.coin_messages.remove(message.id)
    #             await message.clear_reactions()
    #             coins = choice([5, 10, 15])
    #             c.evil_coins += coins
    #             msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} found **{coins} evil coins!** ~{evil_coins_e}"))
    #             # Save it to database
    #             async with self.bot.database() as db:
    #                 await c.save(db)

    #     elif str(payload.emoji) == bunny_e:
    #         if message.id in self.bunny_messages:
    #             #! Quest 4 Complete
    #             await self.bot.get_cog('Quests').get_quest(user=user, quest_no=4, completed=True)
    #             self.bunny_messages.remove(message.id)
    #             await message.clear_reactions()
    #             c.coins += 250
    #             msg = await channel.send(embed=utils.SpecialEmbed(desc=f"{user} Received **250 coins**\nSource: Bunny"))
    #             # Save it to database
    #             async with self.bot.database() as db:
    #                 await c.save(db)

    #     else: 
    #         return

    #     if msg != None:
    #         await sleep(3)
    #         await msg.delete()
    #     else: 
    #         return








    # @Cog.listener('on_message')
    # async def Trait_Handler(self, message):
    #     '''Trait Handler'''

    #     # BETTER NOT BE A DM
    #     if message.guild == None:
    #         return
    #     # Disables Bots
    #     if message.author.bot:
    #         return

    #     # Define some variables
    #     user = message.author
    #     c = utils.Currency.get(user.id)
    #     msg = None
    #     triggered = False
    #     coins = 0
    #     messages = None

    #     #! Red Role (Fire Touch)
    #     if [i for i in user.roles if i.id == self.bot.config['roles']['traits']['red']]:
    #         role = utils.DiscordGet(user.guild.roles, id=self.bot.config['roles']['traits']['red'])
    #         luck = randint(1, 2000)
    #         if luck < 10:
    #             await user.remove_roles(role)
    #             await message.channel.send(embed=utils.SpecialEmbed(desc=f"{user} lost his red color role!"))
    #         if luck < 100:
    #             triggered = True
    #             messages = await message.channel.history(limit=8).flatten()
    #             for message in messages:
    #                 chance = choice([1, 2, 3])
    #                 if chance == 3:
    #                     coins += 25
    #                     c.coins += 25
    #                     await message.add_reaction("🔥")
    #             async with self.bot.database() as db:
    #                 await c.save(db)
    #             await message.channel.send(embed=utils.SpecialEmbed(desc=f"{user} recieved {coins:,} coins!\nSource: Fire Touch - 🔥x 25"))

    #     #! Red Role (Fire Touch)
    #     if [i for i in user.roles if i.id == self.bot.config['roles']['traits']['blue']]:
    #         role = utils.DiscordGet(user.guild.roles, id=self.bot.config['roles']['traits']['blue'])
    #         luck = randint(1, 2000)
    #         if luck < 10:
    #             await user.remove_roles(role)
    #             await message.channel.send(embed=utils.SpecialEmbed(desc=f"{user} lost his blue color role!"))
    #         if luck < 100:
    #             triggered = True
    #             messages = await message.channel.history(limit=12).flatten()
    #             for message in messages:
    #                 chance = choice([1, 2, 3])
    #                 if chance == 3:
    #                     c = utils.Currency.get(user.id)
    #                     coins += 50
    #                     c.coins += 50
    #                     await message.add_reaction("🌊")
    #                     async with self.bot.database() as db:
    #                         await c.save(db)
    #             await message.channel.send(embed=utils.SpecialEmbed(desc=f"{user} gived rewards to random messages!\nSource: Tsunami - 🌊x 50"))

    #     #! Red Role (Fire Touch)
    #     if [i for i in user.roles if i.id == self.bot.config['roles']['traits']['pink']]:
    #         role = utils.DiscordGet(user.guild.roles, id=self.bot.config['roles']['traits']['pink'])
    #         luck = randint(1, 2000)
    #         if luck < 10:
    #             await user.remove_roles(role)
    #             await message.channel.send(embed=utils.SpecialEmbed(desc=f"{user} lost his pink color role!"))
    #         if luck < 100:
    #             triggered = True
    #             messages = await message.channel.history(limit=4).flatten()
    #             for message in messages:
    #                 chance = choice([1, 2, 3])
    #                 if chance == 3:
    #                     if message.author.id == user.id:
    #                         pass
    #                     c = utils.Currency.get(user.id)
    #                     coins += 50
    #                     c.coins += 50
    #                     await message.add_reaction("🍑")
    #                     await message.author.add_roles(role)
    #                     await user.remove_roles(role)
    #                     async with self.bot.database() as db:
    #                         await c.save(db)
    #                     await message.channel.send(embed=utils.SpecialEmbed(desc=f"{user} infected {message.author}!\nSource: Pink-19 - 🍑"))

    #     #! Green Role (Leaf Roulette)
    #     if [i for i in user.roles if i.id == self.bot.config['roles']['traits']['green']]:
    #         role = utils.DiscordGet(user.guild.roles, id=self.bot.config['roles']['traits']['green'])
    #         luck = randint(1, 2000)
    #         if luck < 10:
    #             await user.remove_roles(role)
    #             await message.channel.send(embed=utils.SpecialEmbed(desc=f"{user} lost his green color role!"))
    #         if luck < 100:
    #             triggered = True
    #             messages = await message.channel.history(limit=6).flatten()
    #             for message in messages:
    #                 chance = choice([1, 2, 3, 4, 5, 6, 7, 8])
    #                 if chance == 3:
    #                     if message.author.id == user.id:
    #                         pass
    #                     c = utils.Currency.get(user.id)
    #                     coins += 50
    #                     c.coins += 50
    #                     choices = ['🍁', '🍂', '🍃', '🍀', '🌿', '🌸']
    #                     for choice in choices:
    #                         if choice([1,2]) == 1:
    #                             await message.add_reaction(choice(choices))
    #                     await sleep (7)
    #                     async with self.bot.database() as db:
    #                         await c.save(db)
    #                     await message.channel.send(embed=utils.SpecialEmbed(desc=f"{user} infected {message.author}!\nSource: Pink-19 - 🍑"))



    #     await sleep(7)
    #     #! Clear Reactions
    #     if messages:
    #         for message in messages:
    #             await message.clear_reactions()
















def setup(bot):
    x = item_handler(bot)
    bot.add_cog(x)