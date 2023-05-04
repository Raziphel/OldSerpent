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
            msg = await ch.fetch_message(1103507070210285640)
            msg2 = await ch.fetch_message(1103507080826064938)
            tickets = utils.Items.get_total_tickets()

            embed=Embed(description=f"**__Welcome to the raffle!!!__**\n\n**Prize Pool: {lot.coins:,}x {coin_e}**", color=randint(1, 0xffffff))
            await msg.edit(content=f"**Congrats to the last winner:** <@{lot.last_winner_id}>\nThey won: **{coin_e} {lot.last_amount:,}**",embed=embed)
            
            embed=Embed(description=f"**__Welcome to the lottery store!!!__**\n*You're really fucking bad with money...*", color=randint(1, 0xffffff))
            embed.add_field(name="🍏 -> 5 Tickets", value=f"\n**{coin_e} 5,000x**\n", inline=True)
            embed.add_field(name="🍎 -> 10 Tickets", value=f"\n**{coin_e} 10,000x**\n", inline=True)
            embed.add_field(name="🍐 -> 25 Tickets", value=f"\n**{coin_e} 25,000x**\n", inline=True)
            embed.add_field(name="🍋 -> 50 Tickets", value=f"\n**{coin_e} 50,000x**\n", inline=True)
            embed.add_field(name="🍇 -> 100 Tickets", value=f"\n**{coin_e} 100,000x**\n", inline=True)
            await msg2.edit(content=f"Here you can purchase lottery tickets!  It is a weighted lottery, so the more tickets the higher chances! (refreshes: {counter:,}x)",embed=embed)
            
            await sleep(60) 



    async def lottery(self):
        await self.bot.wait_until_ready()
        counter = 0
        while not self.bot.is_closed():
            lot = utils.Lottery.get(1)
            guild = self.bot.get_guild(self.bot.config['garden_id'])
            ch = guild.get_channel(self.bot.config['channels']['lottery'])
            sorted_ticket_rank = utils.Items.sort_tickets()
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
            if (lot.lot_time + timedelta(days=3)) > dt.now():
                tf = lot.lot_time + timedelta(days=3)
                t = dt(1,1,1) + (tf - dt.now())
                msg = await ch.fetch_message(1103507090389078046)
                await msg.edit(content=f" ", embed=utils.SpecialEmbed(title=f"Lottery Timer", desc=f"**The weekly lottery has:** {t.day} days, {t.hour} hours and {t.minute} minutes remaining!\n\n**Top Ticket Holders:**\n**#1) {user1} 〰️ {floor(rank1.lot_tickets):,} Tickets**\n**#2) {user2} 〰️ {floor(rank2.lot_tickets):,} Tickets**\n**#3) {user3} 〰️ {floor(rank3.lot_tickets):,} Tickets**\n**#4) {user4} 〰️ {floor(rank4.lot_tickets):,} Tickets**\n**#5) {user5} 〰️ {floor(rank5.lot_tickets):,} Tickets**"))


            #! If it is time to do the lottery
            if (lot.lot_time + timedelta(days=3)) < dt.now():
                lot.lot_time = dt.now()
                print("Ran the lottery")

                async with self.bot.database() as db:
                    v = await db('SELECT user_id, lot_tickets FROM items WHERE lot_tickets > 0;')

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
                rc = utils.Currency.get(550474149332516881)

                # now tickets is a list of user ids, where each user ID appears the same amount of times as the tickets they've purchased
                await ch.send(embed=utils.SpecialEmbed(desc=f"The winner of the lottery is: **{winner}**!"))
                lot_winnings = await utils.CoinFunctions.pay_tax(payer=winner, amount=lot.coins)
                c.coins += lot_winnings
                rc.coins -= lot_winnings
                lot.last_winner = winner.id
                lot.last_amount = lot.coins
                lot.coins = 0
                async with self.bot.database() as db:
                    await lot.save(db)
                    await c.save(db)

                for member in guild.members:
                    c = utils.Currency.get(member.id)
                    i.lot_tickets = 0
                    async with self.bot.database() as db:
                        await c.save(db)

            await sleep(60)







    async def lottery_increaser(self):
        await self.bot.wait_until_ready()
        counter = 0
        while not self.bot.is_closed():
            lot = utils.Lottery.get(1)

            lot.coins += 100
            c = utils.Currency.get(550474149332516881)
            c.coins -= 100

            async with self.bot.database() as db:
                await lot.save(db)
                await c.save(db)
            await sleep(3600)







    @Cog.listener('on_raw_reaction_add')
    async def lot_buy(self, payload:RawReactionActionEvent):
            '''Buys item's from the lottery.'''

            # See if I need to deal with it
            if not payload.channel_id == self.bot.config['channels']['lottery']:
                return
            if self.bot.get_user(payload.user_id).bot:
                return

            #! See what the emoji is
            if payload.emoji.is_unicode_emoji():
                emoji = payload.emoji.name 
            else:
                emoji = payload.emoji.id

            coin = self.bot.config['emotes']['coin']
            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            c = utils.Currency.get(payload.user_id)
            i = utils.Items.get(payload.user_id)
            lot = utils.Lottery.get(1)

            item = {"name": "BROKEN OH NO", "coin": -1}

            restricted = utils.DiscordGet(guild.roles, name="Lot Restricted")
            if restricted in user.roles: #! If they try to warn a staff member!
                await user.send(embed=utils.WarningEmbed(title="You are lot restricted"))
                return

            #! Get the correct item
            if emoji == "🍏":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase 5 lottery tickets!\nCost: {coin} 5,000x", footer=" "))
                item['name'] = "5 Tickets"
                item['coin'] = 5000
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    i.lot_tickets += 5
                    lot.coins += item['coin']

            if emoji == "🍎":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase 10 lottery tickets!\nCost: {coin} 10,000x", footer=" "))
                item['name'] = "10 Tickets"
                item['coin'] = 10000
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    i.lot_tickets += 10
                    lot.coins += item['coin']

            if emoji == "🍐":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase 25 lottery tickets!\nCost: {coin} 5,000x", footer=" "))
                item['name'] = "25 Tickets"
                item['coin'] = 25000
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    i.lot_tickets += 25
                    lot.coins += item['coin']

            if emoji == "🍋":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase 50 lottery tickets!\nCost: {coin} 5,000x", footer=" "))
                item['name'] = "50 Tickets"
                item['coin'] = 50000
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    i.lot_tickets += 50
                    lot.coins += item['coin']

            if emoji == "🍇":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase 100 lottery tickets!\nCost: {coin} 5,000x", footer=" "))
                item['name'] = "100 Tickets"
                item['coin'] = 100000
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    i.lot_tickets += 100
                    lot.coins += item['coin']


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
                await user.send(embed=utils.DefaultEmbed(user=user, type="positive", title=f"You have bought {item['name']}!"))
                await self.coin_logs.send(f"**{user}** bought **{item['name']}**!")
            else:       
                await user.send(embed=utils.DefaultEmbed(user=user, type="positive", title=f"Failed to purchase: {item['name']}!"))
                await self.coin_logs.send(f"**{user}** tried to purchase: **{item['name']}**")






    async def purchasing(self, msg, payload, item):
        '''The system for buying in the shop.'''

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        c = utils.Currency.get(user.id)
        coin = self.bot.config['emotes']['coin']


        await msg.add_reaction("✔")
        await msg.add_reaction("❌")
        try:
            check = lambda x, y: y.id == user.id and x.message.id == msg.id and x.emoji in ["✔", "❌"]
            r, _ = await self.bot.wait_for('reaction_add', check=check)
            if r.emoji == "✔":
                if c.coins < item["coin"]:
                    await msg.edit(embed=utils.LogEmbed(type="negative", desc=f"You don't have enough Coins for: `{item['name']}`!\nYou need {item['coin'] - floor(c.coins):,}x {coin}!", footer=" "))
                    return False
                else: return True

            if r.emoji == "❌":
                    await msg.edit(embed=utils.LogEmbed(type="negative", desc=f"Purchase was canceled!", footer=" "))
                    return False


        except TimeoutError:
            await msg.edit('Sorry, but you took too long to respond.  Transaction Canceled.', embed=None)
            return False






def setup(bot):
    x = lottery_handler(bot)
    bot.add_cog(x)