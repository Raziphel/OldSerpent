
#* Discord
from discord.ext.commands import command, Cog
from discord import Embed, PartialEmoji, Message, RawReactionActionEvent, Guild
#* Additions
import math
from random import randint, choice
from asyncio import sleep
from more_itertools import unique_everseen
from datetime import datetime as dt, timedelta

import utils

class Mail_Box(Cog):

    def __init__(self, bot):
        self.bot = bot


    @property  #! The currency logs
    def archive(self):
        return self.bot.get_channel(self.bot.config['channels']['archive']) #?archive log channel



    async def message_embed_author(self, embed_to_get_author_from:Embed, *args, **kwargs):
        '''Gets the author attribute of an embed and the rest of the args go to Messagable.send'''
        try:
            author_str = embed_to_get_author_from.author.icon_url
            author_id = int(author_str.split('/')[4])
            author = self.bot.get_user(author_id)
            await author.send(*args, **kwargs)
        except Exception as e:
            raise e


    async def embed_author_id(self, embed_to_get_author_from:Embed):
        '''Gets the author's id from the embed.'''
        try:
            author_str = embed_to_get_author_from.author.icon_url
            author_id = int(author_str.split('/')[4])
            return author_id
        except Exception as e:
            raise e



    @Cog.listener('on_raw_reaction_add')
    async def mail_system(self, payload:RawReactionActionEvent,):
        '''Deal with mail system'''
        if payload.channel_id != self.bot.config['channels']['mail_box']:
            return
        if self.bot.get_user(payload.user_id).bot:
            return

        guild = self.bot.get_guild(payload.guild_id)
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if len(message.embeds) == 0:
            return 
        emoji = payload.emoji
        #* Check the embed
        embed = message.embeds[0]
        if 'Verification' == embed.footer.text:
                await self.deal_with_verification(message, emoji, embed, payload, guild)
        elif 'Kingussy' == embed.footer.text:
                await self.deal_with_kingussy(message, emoji, embed, payload, guild)
        elif 'Furry' == embed.footer.text:
                await self.deal_with_furry(message, emoji, embed, payload, guild)
        elif 'Adult' == embed.footer.text:
                await self.deal_with_adult(message, emoji, embed, payload, guild)
        elif 'KindaAdult' == embed.footer.text:
                await self.deal_with_adult(message, emoji, embed, payload, guild, kinda=True)


    async def deal_with_verification(self, message:Message, emoji:PartialEmoji, embed:Embed, payload:RawReactionActionEvent, guild:Guild):
        '''Deals with verification'''
        author_id = await self.embed_author_id(embed)
        author = guild.get_member(author_id)
        if author == None: #? if they left the server.
            await message.delete()
            return

        if emoji.name == '✅':
            #! Archive it!
            embed.colour = 0x008800
            await author.send(f"**You have been verified!  Welcome to {guild.name}!**")
            embed.set_footer(text='Verification archived on ' + dt.utcnow().strftime('%a %d %B %H:%M'))
            await self.archive.send(f'Archived by <@{payload.user_id}>.', embed=embed)
            await message.delete()
            #! Verifys the user
            await utils.UserFunction.verify_user(user=author, type="guild")
        elif emoji.name == '🔴':
            check = lambda m: m.channel == message.channel and payload.user_id == m.author.id
            z = await message.channel.send("Why are you declining this verification?")
            try: 
                reason_message = await self.bot.wait_for('message', check=check, timeout=60.0)
                reason = reason_message.content
                await reason_message.delete()
            except Exception: 
                reason = '<No reason given>'
            try: await author.send(f"Your verification has been rejected, for reason `{reason}`. Please try again later.")
            except Exception: pass
            embed.set_footer(text='Verification declined  on ' + dt.utcnow().strftime('%a %d %B %H:%M'))
            #! Archive it!
            await self.archive.send(f'Denied by <@{payload.user_id}>. For reason: {reason}', embed=embed)
            await message.delete()  
            await self.message_embed_author(embed, f"Your verification was declined. For reason: `{reason}`", embed=embed)
            await z.delete()
            #! kick the user



    async def deal_with_kingussy(self, message:Message, emoji:PartialEmoji, embed:Embed, payload:RawReactionActionEvent, guild:Guild):
        '''Deals with kingussy'''
        author_id = await self.embed_author_id(embed)
        author = guild.get_member(author_id)
        if author == None: #? if they left the server.
            await message.delete()
            return

        if emoji.name == '✅':
            #! Archive it!
            embed.colour = 0x008800
            await author.send(f"**You have been verified!  Welcome to Kingussy!**")
            embed.set_footer(text='Verification archived on ' + dt.utcnow().strftime('%a %d %B %H:%M'))
            await self.archive.send(embed=utils.LogEmbed(type="positive", title=f"A Kingussy Application was Accepted!", desc=f'Archived by <@{payload.user_id}>.'))
            await message.delete()
            #! Verifys the user
            await utils.UserFunction.verify_user(user=author, type="alliance")

        elif emoji.name == '🔴':
            check = lambda m: m.channel == message.channel and payload.user_id == m.author.id
            z = await message.channel.send("Why are you declining this verification?")
            try: 
                reason_message = await self.bot.wait_for('message', check=check, timeout=60.0)
                reason = reason_message.content
                await reason_message.delete()
            except Exception: 
                reason = '<No reason given>'
            embed.set_footer(text='Verification declined  on ' + dt.utcnow().strftime('%a %d %B %H:%M'))
            #! Archive it!
            await self.archive.send(embed=utils.LogEmbed(type="negative", title=f"A Kingussy Application was Denied!", desc=f'Archived by <@{payload.user_id}>.'))
            await message.delete()  
            await self.message_embed_author(embed, f"Your verification was declined. For reason: `{reason}`", embed=embed)
            await z.delete()
            #! kick the user




    async def deal_with_furry(self, message:Message, emoji:PartialEmoji, embed:Embed, payload:RawReactionActionEvent, guild:Guild):
        '''Deals with furrys'''
        author_id = await self.embed_author_id(embed)
        author = guild.get_member(author_id)
        if author == None: #? if they left the server.
            await message.delete()
            return

        if emoji.name == '✅':
            #! Archive it!
            embed.colour = 0x008800
            await author.send(f"**You have been verified!  Welcome to Razi's Realm Furrys!**")
            embed.set_footer(text='Verification archived on ' + dt.utcnow().strftime('%a %d %B %H:%M'))
            await self.archive.send(f'Archived by <@{payload.user_id}>.', embed=embed)
            await message.delete()
            #! Verifys the user
            await utils.UserFunction.verify_user(user=author, type="furry")

        elif emoji.name == '🔴':
            check = lambda m: m.channel == message.channel and payload.user_id == m.author.id
            z = await message.channel.send("Why are you declining this verification?")
            try: 
                reason_message = await self.bot.wait_for('message', check=check, timeout=60.0)
                reason = reason_message.content
                await reason_message.delete()
            except Exception: 
                reason = '<No reason given>'
            embed.set_footer(text='Verification declined  on ' + dt.utcnow().strftime('%a %d %B %H:%M'))
            #! Archive it!
            await self.archive.send(f'Denied by <@{payload.user_id}>. For reason: {reason}', embed=embed)
            await message.delete()  
            await self.message_embed_author(embed, f"Your verification was declined. For reason: `{reason}`", embed=embed)
            await z.delete()
            #! kick the user




    async def deal_with_adult(self, message:Message, emoji:PartialEmoji, embed:Embed, payload:RawReactionActionEvent, guild:Guild, kinda:str=False):
        '''Deals with adults'''
        author_id = await self.embed_author_id(embed)
        author = guild.get_member(author_id)
        if author == None: #? if they left the server.
            await message.delete()
            return

        if emoji.name == '✅':
            #! Archive it!
            embed.colour = 0x008800
            await author.send(f"**You have been verified as an adult!**")
            embed.set_footer(text='Verification archived on ' + dt.utcnow().strftime('%a %d %B %H:%M'))
            await self.archive.send(f'Archived by <@{payload.user_id}>.', embed=embed)
            await message.delete()
            #! Verifys the user
            if kinda == False:
                await utils.UserFunction.verify_user(user=author, type="adult")
            else: await utils.UserFunction.verify_user(user=author, type="kindaadult")

        elif emoji.name == '🔴':
            check = lambda m: m.channel == message.channel and payload.user_id == m.author.id
            z = await message.channel.send("Why are you declining this verification?")
            try: 
                reason_message = await self.bot.wait_for('message', check=check, timeout=60.0)
                reason = reason_message.content
                await reason_message.delete()
            except Exception: 
                reason = '<No reason given>'
            embed.set_footer(text='Verification declined  on ' + dt.utcnow().strftime('%a %d %B %H:%M'))
            #! Archive it!
            await self.archive.send(f'Denied by <@{payload.user_id}>. For reason: {reason}', embed=embed)
            await message.delete()  
            await self.message_embed_author(embed, f"Your verification was declined. For reason: `{reason}`", embed=embed)
            await z.delete()
            await utils.UserFunction.verify_user(user=author, type="notadult")
            mod = utils.Moderation.get(member.id)
            mod.child = True



def setup(bot):
    x = Mail_Box(bot)
    bot.add_cog(x)