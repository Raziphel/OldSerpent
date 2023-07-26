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
        self.sparkle_messages = []
        self.bun_msg = 0



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
            chance = randint(1, 25000)
            if chance <= 25:
                message = choice(messages)
                await message.add_reaction("✨")
                self.sparkle_messages.append(message.id)
            elif chance <= 75:
                for x in range(5):
                    message = choice(messages)
                    reaction = await message.add_reaction(self.bot.config['emotes']['bunny'])
                    self.bunny_messages.append(message.id)
            elif chance <= 500:
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
        channel = guild.get_channel(payload.channel_id)
        try:
            message = await channel.fetch_message(payload.message_id)
        except: return
        msg = None

        c = utils.Currency.get(user.id)
        i = utils.Items.get(user.id)
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
                await utils.CoinFunctions.earn(earner=user, amount=coin)
                msg = await channel.send(embed=utils.DefaultEmbed(user=user, desc=f"{user.name} found **{coin} {coin_e}x**"))
                await coin_logs.send(f"**{user}** found **{coin} {coin_e}**")
                #! Quest 1 Complete
                await self.bot.get_cog('Quests').get_quest(user=user, quest_no=1, completed=True)

        elif str(payload.emoji) == bunny_e:
            if message.id in self.bunny_messages:
                self.bunny_messages.remove(message.id)
                await message.clear_reactions()
                coin = choice([200, 250, 300])
                await utils.CoinFunctions.earn(earner=user, amount=coin)
                msg = await channel.send(embed=utils.DefaultEmbed(user=user, desc=f"{user.name} got **{coin} {coin_e}x from a bunny!**"))
                await coin_logs.send(f"**{user}** got **{coin} {coin_e} from a bunny!**")
                #! Quest 4 Complete
                await self.bot.get_cog('Quests').get_quest(user=user, quest_no=4, completed=True)

        elif str(payload.emoji) == "✨":
            if message.id in self.sparkle_messages:
                self.sparkle_messages.remove(message.id)
                await message.clear_reactions()
                coin = choice([1000, 3000, 5000])
                await utils.CoinFunctions.earn(earner=user, amount=coin)
                msg = await channel.send(embed=utils.DefaultEmbed(user=user, desc=f"{user.name} got **{coin} {coin_e}x from a sparkle!**"))
                await coin_logs.send(f"**{user}** got **{coin} {coin_e} from a sparkle!**")

        elif str(payload.emoji) == "🎟":
            if message.id in self.ticket_messages:
                self.ticket_messages.remove(message.id)
                await message.clear_reactions()
                tix = choice([1, 2, 3])
                i.lot_tickets += tix
                msg = await channel.send(embed=utils.DefaultEmbed(user=user, desc=f"{user.name} got **{tix} Lottery Tickets!**"))
                await coin_logs.send(f"**{user}** got **{tix} Lottery Tickets!!**")


        else: 
            return

        #! Save it to database
        async with self.bot.database() as db:
            await c.save(db)
            await i.save(db)

        if msg != None:
            await sleep(5)
            await msg.delete()
        else: 
            return


def setup(bot):
    x = Message_Rewards(bot)
    bot.add_cog(x)