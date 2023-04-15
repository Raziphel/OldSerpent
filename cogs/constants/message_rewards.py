# Discord
# Additions
from asyncio import sleep
from random import choice, randint

from discord import RawReactionActionEvent
from discord.ext.commands import Cog

import utils


class Message_Rewards(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bunny_messages = []
        self.coin_messages = []



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
            chance = randint(1, 2500)
            if chance <= 5:
                for x in range(5):
                    message = choice(messages)
                    reaction = await message.add_reaction(self.bot.config['emotes']['bunny'])
                    self.bunny_messages.append(message.id)
            elif chance <= 40:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emotes']['coin'])
                self.coin_messages.append(message.id)
        except Exception as e:
            print(f'A reward failed to spawn :: {e}')

        await sleep(10)

        try:
            await reaction.remove(self.bot.user)
        except: pass




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
        try:
            message = await channel.fetch_message(payload.message_id)
        except: return
        msg = None

        coin_logs = self.bot.get_channel(self.bot.config['channels']['coin_logs'])

        #! Define Emojis
        bunny_e = "<a:Bunny:703136644366336000>"
        coin_e = self.bot.config['emotes']['coin']

        #! Get the correct item
        if str(payload.emoji) == coin_e:
            if message.id in self.coin_messages:
                self.coin_messages.remove(message.id)
                await message.clear_reactions()
                coin = choice([100, 150, 200, 250, 300])
                await utils.CoinFunctions.earn(earner=message.author, amount=coin)
                msg = await channel.send(embed=utils.DefaultEmbed(user=user, desc=f"{user} found **{coin} {coin_e}x**"))
                await coin_logs.send(f"**{user}** found **{coin} {coin_e}**")

        #! Get the correct item
        elif str(payload.emoji) == bunny_e:
            if message.id in self.bunny_messages:
                self.bunny_messages.remove(message.id)
                await message.clear_reactions()
                coin = choice([100, 150, 250])
                await utils.CoinFunctions.earn(earner=message.author, amount=coin)
                msg = await channel.send(embed=utils.DefaultEmbed(user=user, desc=f"{user} got **{coin} {coin_e}x from a bunny!**"))
                await coin_logs.send(f"**{user}** got **{coin} {coin_e} from a bunny!**")



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
    x = Message_Rewards(bot)
    bot.add_cog(x)