
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
        if payload.channel_id not in self.bot.mail_boxes:
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
        if 'Verification' in embed.footer.text:
            if payload.user_id == self.bot.helpers:
                await self.deal_with_verification(message, emoji, embed, payload, guild)
        elif 'sfw_sona' in embed.footer.text:
            if payload.user_id == self.bot.nsfw_staff:
                await self.deal_with_sfw_sona(message, emoji, embed, payload, guild)



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
            archive = await utils.ChannelFunction.get_log_channel(guild=guild, log="sfw_archive")
            await archive.send(f'Archived by <@{payload.user_id}>.', embed=embed)
            await message.delete()
            #! Verifys the user
            await utils.UserFunction.verify_user(user=author, guild=guild)

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
            archive = await utils.ChannelFunction.get_log_channel(guild=guild, log="sfw_archive")
            await archive.send(f'Denied by <@{payload.user_id}>. For reason: {reason}', embed=embed)
            await message.delete()  
            await self.message_embed_author(embed, f"Your verification was declined. For reason: `{reason}`", embed=embed)
            await z.delete()
            #! kick the user







    async def deal_with_sona(self, message:Message, emoji:PartialEmoji, embed:Embed, payload:RawReactionActionEvent, guild:Guild):
        '''Deals with the accept/deny stage of a character'''
        author_id = await self.embed_author_id(embed)
        author = guild.get_member(author_id)
        if author == None:
            await message.delete()
            return

        if emoji.name == '✅':
            archive = await utils.ChannelFunction.get_log_channel(guild=guild, log="sfw_archive")
            await archive.send(f"The sona of {author.mention} was **approved** by <@{payload.user_id}>")
            await archive.send(embed=utils.ProfileEmbed(type="Sona", sona='sfw', staff=True, user=author))
            await author.send("**Your sona was approved!**")
            sonas = await utils.ChannelFunction.get_log_channel(guild=guild, log="sonas")
            await sonas.send(f"{author.mention}'s sona was accepted!", embed=utils.ProfileEmbed(type="Sona", sona='sfw', staff=True, user=author))
            ch = utils.Sonas.get(author.id)
            ch.verified = True
            async with self.bot.database() as db:
                await ch.save(db)
            await message.delete()

        elif emoji.name in ['🔴', '💜']:
            ch = utils.Sonas.get(author.id)
            await utils.Sonas.delete(user_id=author.id)
            check = lambda m: m.channel == message.channel and payload.user_id == m.author.id
            z = await message.channel.send("Why are you declining that sona?")
            if emoji.name != '💜':
                try: 
                    reason_message = await self.bot.wait_for('message', check=check, timeout=60.0)
                    reason = reason_message.content
                    await reason_message.delete()
                except Exception: 
                    reason = '<No reason given>'
            else: reason = f'Thanks for submitting a sona! However, on Furry Royale, all sona images must be furry art, fan-art / non-main stream anime art, MLP, or Scaley sonas. If you wish to circumvent these requirements, you may become a 5$ patreon to support our server. Otherwise, please resend your sona with an appropriate image. The full guidelines may be viewed in #📜rules📜'

            try: await author.send(f"**Your sona has been rejected, for: `{reason}`. Please try again.**")
            except Exception: pass
            archive = await utils.ChannelFunction.get_log_channel(guild=guild, log="sfw_archive")
            await archive.send(f"The sona of {author.mention} was **declined** by <@{payload.user_id}> for reason: `{reason}`", )
            await archive.send(embed=utils.ProfileEmbed(type="Sona", sona='sfw', staff=True, user=author))
            await z.delete()
            await message.delete()



def setup(bot):
    x = Mail_Box(bot)
    bot.add_cog(x)