
#* Discord
from discord.ext.commands import command, Cog, group, RoleConverter
from discord import Member, Message, User, TextChannel, Role, RawReactionActionEvent, Embed
#* Additions
from asyncio import iscoroutine, gather, sleep
from traceback import format_exc

from random import choice, randint
from math import floor

import utils

class Shop_Handler(Cog):
    def __init__(self, bot):
        self.bot = bot


    @property  #! The currency logs
    def currency_log(self):
        return self.bot.get_channel(self.bot.config['channels']['currency_log'])


    @Cog.listener('on_ready')
    async def shop_msg(self):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['shop_handler']) #? Rules Channel

        msg1 = await ch.fetch_message(959009617155878982) #? Welcome messages
        msg2 = await ch.fetch_message(959009625812901898)
        msg3 = await ch.fetch_message(959009631043190826)
        msg4 = await ch.fetch_message(959009640539099136)
        msg5 = await ch.fetch_message(959009651746304032)
        msg6 = await ch.fetch_message(959018957623406653)

        #* Get the gem emojis
        silver = self.bot.config['emotes']['silver']
        gold = self.bot.config['emotes']['gold']
        emerald = self.bot.config['emotes']['emerald']
        diamond = self.bot.config['emotes']['diamond']
        ruby = self.bot.config['emotes']['ruby']
        sapphire = self.bot.config['emotes']['sapphire']
        amethyst = self.bot.config['emotes']['amethyst']
        crimson = self.bot.config['emotes']['crimson']

        embed1=Embed(title=f"**[- The Ferret's Shop -]**", description=f"**By clicking the coresponding emoji, you will recieve a dm from the bot where you have to accept the transaction.**", color=0x1d89e3)

        embed2=Embed(title=f"**[- Exclusives -]**", description=f"**Items that are purposely made very expensive, due to there value!**", color=0x1d89e3)
        embed2.add_field(name=f"✨ ❧ Discord Nitro", value=f"*Get the 10$ Discord Nitro!*\n**{crimson} 1x**", inline=True)
        embed2.add_field(name=f"⭐ ❧ Discord Nitro Classic", value=f"*Get the 5$ Discord Nitro Classic.*\n**{amethyst} 50x**", inline=True)

        embed3=Embed(title=f"**[- Roles & Perms -]**", description=f"**This is a list of discord related items for sale.**", color=0x1d89e3)

        embed4=Embed(title=f"**[- Abilities -]**", description=f"**Use special abilites on a set cooldown!  (Keep them forever)**", color=0x1d89e3)

        embed5=Embed(title=f"**[- Trait Roles -]**", description=f"**Get temporary roles to enjoy for up to 8 hours. (May not always be 8 hours.)**", color=0x1d89e3)

        embed6=Embed(title=f"**[- Coming Soon -]**", description=f"**Coming Soon!**", color=0x1d89e3)


        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f" ", embed=embed4)
        await msg5.edit(content=f" ", embed=embed5)
        await msg6.edit(content=f" ", embed=embed6)








    @Cog.listener('on_raw_reaction_add')
    async def shop_buy(self, payload:RawReactionActionEvent):
            '''Buys item's from the shop.'''

            #! See if I need to deal with it
            if not payload.channel_id == self.bot.config['channels']['shop_handler']:
                return
            if self.bot.get_user(payload.user_id).bot:
                return

            #! See what the emoji is
            if payload.emoji.is_unicode_emoji():
                emoji = payload.emoji.name 
            else:
                emoji = payload.emoji.id

            #* Get the gem emojis
            silver = self.bot.config['emotes']['silver']
            gold = self.bot.config['emotes']['gold']
            emerald = self.bot.config['emotes']['emerald']
            diamond = self.bot.config['emotes']['diamond']
            ruby = self.bot.config['emotes']['ruby']
            sapphire = self.bot.config['emotes']['sapphire']
            amethyst = self.bot.config['emotes']['amethyst']
            crimson = self.bot.config['emotes']['crimson']

            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            c = utils.Currency.get(user.id)
            bought = False
            item = {"name": "BROKEN OH NO", "ruby": -1, "sapphire": -1, "amethyst": -1, "crimson": -1}

            #? Get the correct item
            if emoji == "✨":
                msg = await user.send(embed=utils.LogEmbed(type="special", title="Purchase Confirmation:", desc=f"Please confirm you would like to purchase Discord Nitro!\nCost: {crimson} 1x", footer=" "))
                item['crimson'] = 1
                item['name'] = "Discord Nitro"
                if await self.purchasing(msg=msg, payload=payload, item=item) == True:
                    await msg.edit(embed=utils.LogEmbed(type="special", title="Purchase Complete", desc=f"Congrats!!!  Omg!  Razi will give you your reward within 24 hours!", footer=" "))
                    bought = True
                    c.crimson -= item['crimson']
                    razi = guild.get_member(self.bot.config['developer'])
                    await razi.send(embed=utils.LogEmbed(type="special", title="Discord Nitro Purchase", desc=f"{user} purchased Discord Nitro!!!!", footer=" "))

            #! Save to databse
            async with self.bot.database() as db:
                await c.save(db)


            if bought == True:
                await self.currency_log.send(embed=utils.LogEmbed(type="positive", title=f"{user} bought {item['name']}!"))
            else: 
                await self.currency_log.send(embed=utils.LogEmbed(type="negative", title=f"{user} failed purchase!", desc=f"{user} tried to purchase: {item['name']}"))

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

        await msg.add_reaction("✔")
        await msg.add_reaction("❌")
        try:
            check = lambda x, y: y.id == user.id and x.message.id == msg.id and x.emoji in ["✔", "❌"]
            r, _ = await self.bot.wait_for('reaction_add', check=check)
            if r.emoji == "✔":
                if c.ruby < item["ruby"]:
                    await msg.edit(embed=utils.LogEmbed(type="negative", desc=f"You don't have enough Ruby for: `{item['name']}`!\nYou need " + str(floor(item["ruby"] - c.ruby)) + " more Ruby!", footer=" "))
                    return False
                elif c.sapphire < item["sapphire"]:
                    await msg.edit(embed=utils.LogEmbed(type="negative", desc=f"You don't have enough Sapphire for: `{item['name']}`!\nYou need " + str(floor(item["sapphire"] - c.sapphire)) + " more Sapphire!", footer=" "))
                    return False
                elif c.amethyst < item["amethyst"]:
                    await msg.edit(embed=utils.LogEmbed(type="negative", desc=f"You don't have enough Amethyst for: `{item['name']}`!\nYou need " + str(floor(item["amethyst"] - c.amethyst)) + " more Amethyst!", footer=" "))
                    return False
                elif c.crimson < item["crimson"]:
                    await msg.edit(embed=utils.LogEmbed(type="negative", desc=f"You don't have enough Crimson for: `{item['name']}`!\nYou need " + str(floor(item["crimson"] - c.crimson)) + " more Crimson!", footer=" "))
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