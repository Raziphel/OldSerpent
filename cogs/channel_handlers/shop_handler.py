
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
    def coin_logs(self):
        return self.bot.get_channel(self.bot.config['channels']['coin_logs'])


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

        embed1=Embed(title=f"**[- Serpent's Toys -]**", description=f"**By clicking the coresponding emoji, you will recieve a dm from the bot where you have to accept the transaction.**\n\n**Exclusive Items:**\n*Items that are purposely made very expensive, due to there value!*", color=0x47F5DB)
        embed1.add_field(name=f"✨ ❧ Discord Nitro", value=f"*Get the 10$ Discord Nitro!*\n\n**{coin} 1,000,000x**", inline=True)

        embed2=Embed(title=f"**[- Roles & Perms -]**", description=f"**This is a list of discord related items for sale.**", color=0x47B9F5)
        embed2.add_field(name=f"📚 ❧ Library Pass", value=f"**{coin} 25,000x**\n\n**Get access to all of the server's logs!**\n*(Full Transparency from all users)*", inline=True)
        embed2.add_field(name=f"🎫 ❧ Image Pass", value=f"**{coin} 20,000x**\n\n**Get permission for images & embeds in General Chats.**", inline=True)
        embed2.add_field(name=f"🎁 ❧ Special Channels", value=f"**{coin} 5,000x**\n\n**Get permission to the XK Class channels.**\n*(Fun/Stupid/Random channels)*", inline=True)
        embed2.add_field(name=f"💀 ❧ Auto-Mod Bypass", value=f"**{coin} 100,000x**\n\n**No longer have to worry about the discord's auto moderation.**", inline=True)


        embed3=Embed(title=f"**[- Abilities & Items -]**", description=f"**Use special abilites on a set cooldown! (Some are Permenant.)**", color=0x475FF5)
        embed3.add_field(name=f"💎 ❧ Daily Bonus", value=f"**{coin} 40,000x**\n\n**Get a bonus with every daily!**\n*(Doesn't get better with more dailys)*", inline=True)
        embed3.add_field(name=f"🧤 ❧ Thief Gloves", value=f"**{coin} 20,000x**\n\n**Get 5 thief gloves!**\n*(Let's you steal coins from people!)*", inline=True)
        
        embed4=Embed(title=f"**[- In-Server Purchases -]**", description=f"**Purchases that are for the SCP servers!**", color=0xB347F5)
        embed4.add_field(name=f"🧶 ❧ Coin Lord", value=f"**{coin} 250,000x**\n\n**Get the orange `Coin Lord Badge` on the SCP servers!**", inline=True)
        embed4.add_field(name=f"🎆 ❧ Bottom Dweller", value=f"**{coin} 100,000x**\n\n**Get the pink `Bottom Dweller Badge` on the SCP servers!**", inline=True)
        embed4.add_field(name=f"🧨 ❧ Toxic", value=f"**{coin} 50,000x**\n\n**Get the green `Toxic Badge` on the SCP servers!**", inline=True)
        
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
            mod = utils.Moderation.get(user.id)
            day = utils.Daily.get(user.id)
            items = utils.Items.get(user.id)
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
                if mod.image_banned == True:
                    await user.send(embed=utils.LogEmbed(type="special", title="IMAGE BANNED", desc=f"You have been banned from ever being able to have an image pass! <3", footer=" "))
                    return
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
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase the Special Channels!\nCost: {coin} 5,000x", footer=" "))
                item['coin'] = 5000
                item['name'] = "Special Channels"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Special Channels!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    special = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['specials'])
                    await user.add_roles(special, reason="Given the Special Channels role.")

            if emoji == "💀":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase the auto-mod bypass!\nCost: {coin} 100,000x", footer=" "))
                item['coin'] = 100000
                item['name'] = "Auto-Mod Bypass"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Auto-mod bypass!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    automod = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['automod'])
                    await user.add_roles(automod, reason="Given Auto-mod bypass role.")

            if emoji == "💎":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase a Daily Bonus!\nCost: {coin} 40,000x", footer=" "))
                item['coin'] = 40000
                item['name'] = "Daily Bonus"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased a daily bonus!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    day.premium = True

            if emoji == "🧤":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase 5 thief gloves!\nCost: {coin} 20,000x", footer=" "))
                item['coin'] = 20000
                item['name'] = "5 thief gloves"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased 5 thief gloves!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    items.thief_gloves += 5

            if emoji == "🧶":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase the Coin Lord badge.\nCost: {coin} 250,000x", footer=" "))
                item['coin'] = 250000
                item['name'] = "Coin Lord Badge"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Lord Badge on SCP servers!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    coin_goblin = utils.DiscordGet(guild.roles, id=1069865257931132938)
                    await user.add_roles(coin_goblin, reason="Given a Coin Lord role.")

            if emoji == "🎆":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase the Bottom Dweller badge!\nCost: {coin} 100,000x", footer=" "))
                item['coin'] = 100000
                item['name'] = "Bottom Dweller Badge"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Bottom Dweller Badge on SCP servers!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    bottom = utils.DiscordGet(guild.roles, id=1085838138183798906)
                    await user.add_roles(bottom, reason="Given a Coin Goblin role.")


            if emoji == "🧨":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase a Daily Bonus!\nCost: {coin} 50,000x", footer=" "))
                item['coin'] = 50000
                item['name'] = "Toxic Badge"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats! Ya purchased the Goblin Badge on SCP servers!", footer=" "))
                    bought = True
                    await utils.CoinFunctions.pay_for(payer=user, amount=item['coin'])
                    coin_goblin = utils.DiscordGet(guild.roles, id=1085838699469733939)
                    await user.add_roles(coin_goblin, reason="Given a Toxic role.")



            #! Save to databse
            async with self.bot.database() as db:
                await c.save(db)
                await day.save(db)
                await mod.save(db)
                await items.save(db)


            if bought == True:
                await self.coin_logs.send(f"**{user}** bought **{item['name']}**!")
            else: 
                await self.coin_logs.send(f"**{user}** tried to purchase: **{item['name']}**")

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