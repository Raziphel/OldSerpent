
#* Discord
from math import floor

from discord import RawReactionActionEvent, Embed
from discord.ext.commands import Cog

import utils


# * Additions

class Shop_Handler(Cog):
    def __init__(self, bot):
        self.bot = bot


    @property  #! The currency logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['channels']['server'])


    @Cog.listener('on_ready')
    async def shop_msg(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['shop']) #? Rules Channel

        msg1 = await ch.fetch_message(959009617155878982) #? Welcome messages
        msg2 = await ch.fetch_message(959009625812901898)
        msg3 = await ch.fetch_message(959009631043190826)
        msg4 = await ch.fetch_message(959009640539099136)
        msg5 = await ch.fetch_message(959009651746304032)

        #* Get the coin emojis
        coin = self.bot.config['emotes']['coin']


        embed1=Embed(title=f"**[- The Realm's Shop -]**", description=f"**By clicking the coresponding emoji, you will recieve a dm from the bot where you have to accept the transaction.**\n\n**Exclusive Items:**\n*Items that are purposely made very expensive, due to there value!*", color=0x47F5DB)
        embed1.add_field(name=f"✨ ❧ Discord Nitro", value=f"*Get the 10$ Discord Nitro!*\n\n**{coin} 1,000,000x**", inline=True)

        embed2=Embed(title=f"**[- Roles & Perms -]**", description=f"**This is a list of discord related items for sale.**", color=0x47B9F5)
        embed2.add_field(name=f"📚 ❧ Library Pass", value=f"**{coin} 25,000x**\n\n**Get access to all of the server's logs!**\n*(Full Transparency from all users)*", inline=True)
        embed2.add_field(name=f"🎫 ❧ Image Pass", value=f"**{coin} 20,000x**\n\n**Get permission for images & embeds in General Chats.**", inline=True)
        embed2.add_field(name=f"🎁 ❧ XKClass Channels", value=f"**{coin} 5,000x**\n\n**Get permission to the XK Class channels.**\n*(Fun/Stupid/Random channels)*", inline=True)


        embed3=Embed(title=f"**[- Abilities & Items -]**", description=f"**Use special abilites on a set cooldown! (Some are Permenant.)**", color=0x475FF5)
        embed3.add_field(name=f"💎 ❧ Daily Bonus", value=f"**{coin} 40,000x**\n\n**Get a bonus with every daily!**\n*(Doesn't get better with more dailys)*", inline=True)
        
        embed4=Embed(title=f"**[- SCP:SL Items -]**", description=f"**Purchases that are for the SCP servers!**", color=0xB347F5)
        embed4.add_field(name=f"🧶 ❧ Coin Goblin", value=f"**{coin} 50,000x**\n\n**Get the `Goblin Badge` on the SCP servers!**", inline=True)
        
        embed5=Embed(title=f"**[- Coming Soon -]**", description=f"**Coming Soon!**", color=0xF54747)


        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f" ", embed=embed4)
        await msg5.edit(content=f" ", embed=embed5)







    @Cog.listener('on_raw_reaction_add')
    async def shop_buy(self, payload:RawReactionActionEvent):
            '''Buys item's from the shop.'''

            #! See if I need to deal with it
            if not payload.channel_id == self.bot.config['channels']['shop']:
                return
            if self.bot.get_user(payload.user_id).bot:
                return

            #! See what the emoji is
            if payload.emoji.is_unicode_emoji():
                emoji = payload.emoji.name 
            else:
                emoji = payload.emoji.id

            #* Get the coin emojis
            coin = self.bot.config['emotes']['coin']


            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            c = utils.Currency.get(user.id)
            day = utils.Daily.get(user.id)
            bought = False
            item = {"name": "BROKEN OH NO", "coin": -1}
            #? Get the correct item
            if emoji == "✨":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase Discord Nitro!\nCost: {coin} 1,000,000x", footer=" "))
                item['coin'] = 1000000
                item['name'] = "Discord Nitro"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats!!!  Razi will give you your reward within 24 hours!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    razi = guild.get_member(self.bot.config['developers']['razi'])
                    await razi.send(embed=utils.LogEmbed(type="special", title="Discord Nitro Purchase", desc=f"{user} purchased Discord Nitro!!!!", footer=" "))

            if emoji == "📚":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase a Library Pass!\nCost: {coin} 25,000x", footer=" "))
                item['coin'] = 25000
                item['name'] = "Library Pass"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased a Library pass!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    library_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['library_pass'])
                    await user.add_roles(library_pass, reason="Given a Library Pass role.")

            if emoji == "🎫":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase a Image Pass!\nCost: {coin} 20,000x", footer=" "))
                item['coin'] = 20000
                item['name'] = "Image Pass"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased a Image pass!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    image_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['image_pass'])
                    await user.add_roles(image_pass, reason="Given a Image Pass role.")

            if emoji == "🎁":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase a XKClass Channels!\nCost: {coin} 5,000x", footer=" "))
                item['coin'] = 5000
                item['name'] = "XKClass Channels"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased a XKClass Channels!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    image_pass = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['xkclass'])
                    await user.add_roles(image_pass, reason="Given a XKClass Channels role.")

            if emoji == "💎":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase a Daily Bonus!\nCost: {coin} 40,000x", footer=" "))
                item['coin'] = 40000
                item['name'] = "Daily Bonus"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased a daily bonus!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    day.premium = True

            if emoji == "🧶":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase a Daily Bonus!\nCost: {coin} 50,000x", footer=" "))
                item['coin'] = 50000
                item['name'] = "Coin Goblin Badge"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Goblin Badge on SCP servers!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    coin_goblin = utils.DiscordGet(guild.roles, id=1069865257931132938)
                    await user.add_roles(coin_goblin, reason="Given a Coin Goblin role.")


            #! Save to databse
            async with self.bot.database() as db:
                await c.save(db)
                await day.save(db)


            if bought == True:
                await self.discord_log.send(embed=utils.LogEmbed(type="positive", title=f"{user} bought {item['name']}!"))
            else: 
                await self.discord_log.send(embed=utils.LogEmbed(type="negative", title=f"{user} failed purchase!", desc=f"{user} tried to purchase: {item['name']}"))

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
    x = Shop_Handler(bot)
    bot.add_cog(x)