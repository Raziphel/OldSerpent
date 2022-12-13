# Discord
from discord.ext.commands import command, Cog, BucketType, group, RoleConverter
from discord import Member, Message, User, Embed, TextChannel, Role, RawReactionActionEvent
# Additions
from asyncio import iscoroutine, gather, sleep
from traceback import format_exc
from datetime import datetime as dt
from datetime import timedelta
from math import floor
from random import choice, randint

import utils

class lottery_handler(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.lott_msg())
        self.bot.loop.create_task(self.lottery_increaser())
        self.bot.loop.create_task(self.lottery())


    async def lott_msg(self):
        '''Edits the shops lottery message!'''
        await self.bot.wait_until_ready()
        counter = 0
        while not self.bot.is_closed():
            #! Define emotes

            coin_e = self.bot.config['emotes']['coin']

            counter += 1
            lot = utils.Lottery.get(1)
            guild = self.bot.get_guild(self.bot.config['garden_id'])
            ch = guild.get_channel(self.bot.config['channels']['lottery'])
            msg = await ch.fetch_message(1052128489303707698)
            msg2 = await ch.fetch_message(1052128498019479562)
            tickets = utils.Currency.get_total_tickets()

            embed=Embed(description=f"**__Welcome to the raffle!!!__**\n\n*Current Prize Pool: {lot.coins:,}x {coin_e}", color=0xff00ff)
            await msg.edit(content=f"**Congrats to the last winner:** <@{lot.last_winner_id}>\nThey won: **{coin_e} {lot.last_amount:,}** | **{evil_coin_e} {floor(lot.last_amount/1000):,}** ",embed=embed)
            
            embed=Embed(description=f"**__Welcome to the lottery store!!!__**\n*You're really fucking bad with money...*", color=0xff00ff)
            embed.add_field(name="🍏 25 Tickets", value=f"**{coin_e} : 2,000**", inline=False)
            embed.add_field(name="🍎 50 Tickets", value=f"**{coin_e} : 3,500**", inline=False)
            embed.add_field(name="🍐 100 Tickets", value=f"**{coin_e} : 6,000**", inline=False)
            embed.add_field(name="🍋 200 Tickets", value=f"**{coin_e} : 10,000**", inline=False)
            embed.add_field(name="🍇 500 Tickets", value=f"**{coin_e} : 25,000**", inline=False)
            await msg2.edit(content=f"Here you can purchase lottery tickets!  It is a weighted lottery, so the more tickets the higher chances! (refreshes: {counter:,}x)",embed=embed)
            
            await sleep(60) 



    async def lottery(self):
        await self.bot.wait_until_ready()
        counter = 0
        while not self.bot.is_closed():
            lot = utils.Lottery.get(1)
            guild = self.bot.get_guild(self.bot.config['garden_id'])
            ch = guild.get_channel(1046611360890503238)
            sorted_ticket_rank = utils.Currency.sort_tickets()
            rank1 = sorted_ticket_rank[0]
            rank2 = sorted_ticket_rank[1]
            rank3 = sorted_ticket_rank[2]
            rank4 = sorted_ticket_rank[3]
            rank5 = sorted_ticket_rank[4]
            user1 = self.bot.get_user(rank1.user_id)
            user2 = self.bot.get_user(rank2.user_id)
            user3 = self.bot.get_user(rank3.user_id)
            user4 = self.bot.get_user(rank4.user_id)
            user5 = self.bot.get_user(rank5.user_id)

            if lot.lot_time == None:
                lot.lot_time = dt.now()
                async with self.bot.database() as db:
                    await lot.save(db)

            #! not time for the lottery
            if (lot.lot_time + timedelta(days=7)) > dt.now():
                tf = lot.lot_time + timedelta(days=7)
                t = dt(1,1,1) + (tf - dt.now())
                msg = await ch.fetch_message(1052129731224535080)
                await msg.edit(content=f" ", embed=utils.SpecialEmbed(title=f"Lottery Timer", desc=f"**The weekly lottery has:** {t.day} days, {t.hour} hours and {t.minute} minutes remaining!\n\n**Top Ticket Holders:**\n**#1) {user1}** 〰️ {floor(rank1.lot_tickets):,}\n**#2) {user2}** 〰️ {floor(rank2.lot_tickets):,}\n**#3) {user3}** 〰️ {floor(rank3.lot_tickets):,}\n**#4) {user4}** 〰️ {floor(rank4.lot_tickets):,}\n**#5) {user5}** 〰️ {floor(rank5.lot_tickets):,}"))


            #! If it is time to do the lottery
            if (lot.lot_time + timedelta(days=7)) < dt.now():
                lot.lot_time = dt.now()
                print("Ran the lottery")

                async with self.bot.database() as db:
                    v = await db('SELECT user_id, lot_tickets FROM currency WHERE lot_tickets > 0;')

                # make a list to put people in
                all_tickets = []

                # go through each database entry
                for row in v:

                    # get the data
                    user_id = row['user_id']
                    amount = row['lot_tickets']

                    # add them to the list AMOUNT times
                    for i in range(amount):
                        all_tickets.append(user_id)

                # Loop until you get a user that's on the server
                winner = None 
                while winner is None and len(all_tickets) > 0:
                    winner_id = choice(all_tickets)
                    winner = guild.get_member(winner_id)
                    if winner == None: 
                        while winner_id in all_tickets:
                            tickets.remove(winner_id)

                # No tickets or no valid user
                if winner is None:
                    await ch.send(embed=utils.SpecialEmbed(desc=f"There were no winners.  Just like Africa."))
                    async with self.bot.database() as db:
                        await lot.save(db)
                    return

                c = utils.Currency.get(winner.id)
                rc = utils.Currency.get(self.bot.user.id)

                # now tickets is a list of user ids, where each user ID appears the same amount of times as the tickets they've purchased
                await ch.send(embed=utils.SpecialEmbed(desc=f"The winner of the lottery is: **{winner}**!"))
                role = utils.DiscordGet(guild.roles, name="Lot Restricted")
                await winner.add_roles(role, reason="Won the 24 hour raffle~")
                lot_winnings = await utils.CoinFunctions.pay_tax(payer=winner, amount=lot.coins)
                c.coins += lot_winnings
                rc.coins -= lot_winnings
                c.evil_coins += floor(lot.coins/1000)
                lot.last_winner = winner.id
                lot.last_amount = lot.coins
                lot.coins = 0
                async with self.bot.database() as db:
                    await lot.save(db)
                    await c.save(db)

                for member in guild.members:
                    c = utils.Currency.get(member.id)
                    c.lot_tickets = 0
                    async with self.bot.database() as db:
                        await c.save(db)

            await sleep(60)







    async def lottery_increaser(self):
        await self.bot.wait_until_ready()
        counter = 0
        while not self.bot.is_closed():
            lot = utils.Lottery.get(1)

            lot.coins += 50

            async with self.bot.database() as db:
                await lot.save(db)
            await sleep(3600)







    @Cog.listener('on_raw_reaction_add')
    async def lot_buy(self, payload:RawReactionActionEvent):
            '''Buys item's from the lottery.'''

            # See if I need to deal with it
            if not payload.channel_id == 703457272730353714:
                return
            if self.bot.get_user(payload.user_id).bot:
                return

            #! See what the emoji is
            if payload.emoji.is_unicode_emoji():
                emoji = payload.emoji.name 
            else:
                emoji = payload.emoji.id

            guild = self.bot.get_guild(payload.guild_id)
            c = utils.Currency.get(payload.user_id)
            member = guild.get_member(payload.user_id)
            lot = utils.Lottery.get(1)

            item = None
            bought = False


            restricted = utils.DiscordGet(guild.roles, name="Lot Restricted")
            if restricted in member.roles: #! If they try to warn a staff member!
                await member.send(embed=utils.WarningEmbed(title="You are lot restricted"))
                return

            #! Get the correct item
            if emoji == "🍏":
                item = "25 Tickets"
                cost = 2000
                if c.coins >= cost:
                    bought = True
                    c.coins -= cost
                    c.lot_tickets += 25
                    lot.coins += cost

            if emoji == "🍎":
                item = "50 Tickets"
                cost = 3500
                if c.coins >= cost:
                    bought = True
                    c.coins -= cost
                    c.lot_tickets += 50
                    lot.coins += cost

            if emoji == "🍐":
                item = "100 Tickets"
                cost = 6000
                if c.coins >= cost:
                    bought = True
                    c.coins -= cost
                    c.lot_tickets += 100
                    lot.coins += cost

            if emoji == "🍋":
                item = "200 Tickets"
                cost = 10000
                if c.coins >= cost:
                    bought = True
                    c.coins -= cost
                    c.lot_tickets += 200
                    lot.coins += cost

            if emoji == "🍇":
                item = "500 Tickets"
                cost = 25000
                if c.evil_coins >= cost:
                    bought = True
                    c.coins -= cost
                    c.lot_tickets += 500
                    lot.coins += 25000

            if emoji == "🍪":
                role = utils.DiscordGet(guild.roles, name="Lot Updates~")
                if len([i for i in member.roles if i.name == "Lot Updates~"]) < 1:
                    item = "Lottery Updates"
                    await member.add_roles(role, reason="Lot Updates~")
                else: 
                    item = "Lottery Updates Removal"
                    bought = False
                    await member.remove_roles(role, reason="Lot Updates~")

            #! Save to databse
            async with self.bot.database() as db:
                await c.save(db)
                await lot.save(db)

            #! Check to see total reactions on the message
            channel_id = payload.channel_id
            channel = self.bot.get_channel(channel_id)
            async for message in channel.history():
                if message.id == payload.message_id:
                    break 
            if message.id != payload.message_id:
                return  # Couldn't find message in channel history

            # See total reactions
            emoji = [i.emoji for i in message.reactions]
            if sum([i.count for i in message.reactions]) > 69:
                await message.clear_reactions()
            for e in emoji:
                await message.add_reaction(e)

            if bought == True:
                if item == "Lottery Updates":
                    await member.send(embed=utils.LogEmbed(type="positive", title=f"You have signed up for {item}!"))        
                    return            

                await member.send(embed=utils.LogEmbed(type="positive", title=f"You have bought {item}!"))
            else: 
                if item == "Lottery Updates":
                    await member.send(embed=utils.LogEmbed(type="positive", title=f"You have signed out for {item}!"))        
                    return          

                await member.send(embed=utils.LogEmbed(type="positive", title=f"Failed to purchase: {item}!"))



def setup(bot):
    x = lottery_handler(bot)
    bot.add_cog(x)