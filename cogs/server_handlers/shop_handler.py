
#* Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter
from discord import Member, Message, User, TextChannel, Role, RawReactionActionEvent, Embed
import utils
#* Additions
from asyncio import iscoroutine, gather, sleep
from traceback import format_exc
from math import floor
from random import randint
from datetime import datetime as dt, timedelta

import utils

class shop_handler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #! The members logs
    def members_log(self):
        return self.bot.get_channel(self.bot.config['channels']['members_log']) 


    @Cog.listener('on_ready')
    async def shop_msg(self):
        ch = self.bot.get_channel(self.bot.config['channels']['shop_handler'])

        msg1 = await ch.fetch_message(959009617155878982) #? Welcome messages
        msg2 = await ch.fetch_message(959009625812901898)
        msg3 = await ch.fetch_message(959009631043190826)
        msg4 = await ch.fetch_message(959009640539099136)
        msg5 = await ch.fetch_message(959009651746304032)
        msg6 = await ch.fetch_message(959018957623406653)

        #* Get the gem emojis
        emerald = self.bot.config['emotes']['emerald']
        diamond = self.bot.config['emotes']['diamond']
        ruby = self.bot.config['emotes']['ruby']
        sapphire = self.bot.config['emotes']['sapphire']
        amethyst = self.bot.config['emotes']['amethyst']
        crimson = self.bot.config['emotes']['crimson']

        embed1=Embed(title=f"**[- The Maiden's Shop -]**", description=f"**Welcome to your one stop place for all your purchasables in The Cult!\nYou will find anything that has price tag attached right here!\nAbsolutely No Refunds!**", color=0x1d89e3)

        embed2=Embed(title=f"**[- Gem miners -]**", description=f"**Miners will generate you gems every hour; Be warned expensive gems generate at a much slower rate.**", color=0x1d89e3)
        embed2.add_field(name=f"❧ Emerald Miner", value=f"*Generates 2 Emeralds every 8 hours.*\n**10,000x {emerald}**", inline=True)
        embed2.add_field(name=f"❧ Diamond Miner", value=f"*Generates 0.5 Diamond every 8 hours.*\n**1,000x {emerald}**", inline=True)
        embed2.add_field(name=f"❧ Ruby Miner", value=f"*Generates 0.25 Ruby every 8 hours.*\n**1,000x {diamond}**", inline=True)
        embed2.add_field(name=f"❧ Sapphire Miner", value=f"*Generates 0.1 Sapphire every 8 hours.*\n**1,000x {ruby}**", inline=True)
        embed2.add_field(name=f"❧ Amethyst Miner", value=f"*Generates 0.05 Amethyst every 8 hours.*\n**1,000x {sapphire}**", inline=True)
        embed2.add_field(name=f"❧ Crimson Miner", value=f"*Generates 0.01 Crimson every 8 hours.*\n**1,000x {amethyst}**", inline=True)

        embed3=Embed(title=f"**[- Roles & Perms -]**", description=f"**This is a list of discord related items for sale.**", color=0x1d89e3)
        embed3.add_field(name=f"❧ Image Key", value=f"*Allows you to post images and embed links in most channels.*\n**2,000x {diamond}**", inline=True)

        embed4=Embed(title=f"**[- Abilities -]**", description=f"**Use special abilites on a set cooldown!  (Keep them forever)**", color=0x1d89e3)

        embed5=Embed(title=f"**[- Trait Roles -]**", description=f"**Get temporary roles to enjoy for up to 8 hours. (May not always be 8 hours.)**", color=0x1d89e3)
        embed5.add_field(name="🍎 ❧ Fire Touch", value="**Red Role** - *Make people's messages around you randomly catch fire, for your reward!*\n**1,000x {emerald}**", inline=True)
        embed5.add_field(name="🌊 ❧ Tsunami", value="**Blue Role** - *Flood a channel out of no where, for everyones reward!*\n**1,000x {emerald}**", inline=True)
        embed5.add_field(name="🍑 ❧ Pink-19", value="**Pink Role** - *Infect other people with the role, curing yourself.*\n**1,000x {diamond}**", inline=True)
        embed5.add_field(name="🍁 ❧ Leaf Roulette", value="**Green Role** - *Get as many leafs as possible!*\n**1,000x {emerald}**", inline=True)


        embed6=Embed(title=f"**[- Coming Soon -]**", description=f"**Coming Soon!**", color=0x1d89e3)




        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f" ", embed=embed4)
        await msg5.edit(content=f" ", embed=embed5)
        await msg6.edit(content=f" ", embed=embed6)





    @Cog.listener('on_raw_reaction_add')
    async def shop(self, payload:RawReactionActionEvent):
            '''Buys item's from the shop.'''

            if self.bot.connected == False:
                return

            # See if I need to deal with it
            if not payload.channel_id == self.bot.config['channels']['shop_handler']:
                return
            if self.bot.get_user(payload.user_id).bot:
                return

            # See what the emoji is
            if payload.emoji.is_unicode_emoji():
                emoji = payload.emoji.name 
            else:
                emoji = payload.emoji

            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            c = utils.Currency.get(member.id)
            m = utils.Miners.get(member.id)


            #* Get the gem emojis
            emerald = self.bot.config['emotes']['emerald']
            diamond = self.bot.config['emotes']['diamond']
            ruby = self.bot.config['emotes']['ruby']
            sapphire = self.bot.config['emotes']['sapphire']
            amethyst = self.bot.config['emotes']['amethyst']
            crimson = self.bot.config['emotes']['crimson']


            if str(emoji) == emerald:
                if c.emerald <= 10000:
                    await member.send(embed=utils.DefualtEmbed(title=f"You do not have the required gems to purchase that!"))
                    return
                elif m.emerald > 9:
                    await member.send(embed=utils.DefualtEmbed(title=f"You already have 10 miners of that type."))
                    return
                c.emerald -= 10000
                m.emerald += 1
                await member.send(embed=utils.DefualtEmbed(title=f"You purchased a Emerald Miner!"))

            elif str(emoji) == diamond:
                if c.emerald <= 1000:
                    await member.send(embed=utils.DefualtEmbed(title=f"You do not have the required gems to purchase that!"))
                    return
                elif m.diamond > 8:
                    await member.send(embed=utils.DefualtEmbed(title=f"You already have 9 miners of that type."))
                    return
                c.emerald -= 1000
                m.diamond += 1
                await member.send(embed=utils.DefualtEmbed(title=f"You purchased a Diamond Miner!"))

            elif str(emoji) == ruby:
                if c.diamond <= 1000:
                    await member.send(embed=utils.DefualtEmbed(title=f"You do not have the required gems to purchase that!"))
                    return
                elif m.ruby > 7:
                    await member.send(embed=utils.DefualtEmbed(title=f"You already have 8 miners of that type."))
                    return
                c.diamond -= 10000
                m.ruby += 1
                await member.send(embed=utils.DefualtEmbed(title=f"You purchased a Ruby Miner!"))

            elif str(emoji) == sapphire:
                if c.ruby <= 1000:
                    await member.send(embed=utils.DefualtEmbed(title=f"You do not have the required gems to purchase that!"))
                    return
                elif m.sapphire > 6:
                    await member.send(embed=utils.DefualtEmbed(title=f"You already have 7 miners of that type."))
                    return
                c.ruby -= 1000
                m.sapphire += 1
                await member.send(embed=utils.DefualtEmbed(title=f"You purchased a Sapphire Miner!"))

            elif str(emoji) == amethyst:
                if c.sapphire <= 1000:
                    await member.send(embed=utils.DefualtEmbed(title=f"You do not have the required gems to purchase that!"))
                    return
                elif m.amethyst > 5:
                    await member.send(embed=utils.DefualtEmbed(title=f"You already have 6 miners of that type."))
                    return
                c.sapphire -= 1000
                m.amethyst += 1
                await member.send(embed=utils.DefualtEmbed(title=f"You purchased a Amethyst Miner!"))

            elif str(emoji) == crimson:
                if c.amethyst <= 1000:
                    await member.send(embed=utils.DefualtEmbed(title=f"You do not have the required gems to purchase that!"))
                    return
                elif m.crimson > 4:
                    await member.send(embed=utils.DefualtEmbed(title=f"You already have 5 miners of that type."))
                    return
                c.amethyst -= 1000
                m.crimson += 1
                await member.send(embed=utils.DefualtEmbed(title=f"You purchased a Crimson Miner!"))

            elif emoji == "🔑":
                if c.diamond <= 2000:
                    await member.send(embed=utils.DefualtEmbed(title=f"You do not have the required gems to purchase that!"))
                    return
                else:
                    c.diamond -= 2000
                    role = utils.DiscordGet(guild.roles, name="Images 🔑")
                    await member.add_roles(role, reason="Item Bought!")
                    await member.send(f"You bought an Images Key!")
                    await self.members_log.send(embed=utils.LogEmbed(type="positive", title=f"Item Purchase", desc=f"{member} purchased Gen Images Key!"))



            # Save the shit
            async with self.bot.database() as db:
                await c.save(db)
                await m.save(db)


            # Check to see total reactions on the message
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






def setup(bot):
    x = shop_handler(bot)
    bot.add_cog(x)