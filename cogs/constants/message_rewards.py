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
        messages = await message.channel.history(limit=8).flatten()

        #! Give them some rewards!
        try:
            chance = randint(1, 750)
            if chance <= 3:
                message = choice(messages)
                msg = await message.channel.send(embed=utils.DefualtEmbed(user=user, desc=f"**Random Tip:** {choice(utils.Tips)}", footer="🍀"))
                await sleep(10)
                await msg.delete()
            elif chance <= 35:
                message = choice(messages)
                await message.add_reaction(self.bot.config['emotes']['coin'])
                self.coin_messages.append(message.id)
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


        #! Define Emojis
        bunny_e = "<a:Bunny:703136644366336000>"
        coin_e = self.bot.config['emotes']['coin']

        #! Get the correct item
        if str(payload.emoji) == coin_e:
            if message.id in self.coin_messages:
                self.coin_messages.remove(message.id)
                await message.clear_reactions()
                coin = choice([100, 150, 200, 250, 300])
                coin = await utils.CoinFunctions.pay_tax(payer=user, amount=coin)
                c.coins += coin
                c.coins_earned += coin
                msg = await channel.send(embed=utils.DefualtEmbed(user=user, desc=f"{user} found **{coin} {coin_e}x**"))

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