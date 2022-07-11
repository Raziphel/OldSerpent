
#* Discord
from discord.ext.commands import command, Cog
from discord.utils import get
#* Additions
import math
from random import randint, choice
from config.lists.welcomes import Welcomes

import utils

class Logging(Cog):

    def __init__(self, bot):
        self.bot = bot

    @property  #! The Server logs
    def bot_log(self):
        return self.bot.get_channel(self.bot.config['channels']['bot_log']) 

    @property  #! The members logs
    def members_log(self):
        return self.bot.get_channel(self.bot.config['channels']['members_log']) 

    @property  #! The message logs
    def message_log(self):
        return self.bot.get_channel(self.bot.config['channels']['message_log']) 

    @property  #! The currency logs
    def currency_log(self):
        return self.bot.get_channel(self.bot.config['channels']['currency_log'])

    @property  #! The welcome logs
    def welcome_log(self):
        return self.bot.get_channel(self.bot.config['channels']['greetings'])



    #! Welcome channel 
    @Cog.listener()
    async def on_member_join(self, member):
        if self.welcome_log == None: return #! Fail silently
        greeting = choice(Welcomes)
        desc = f'Welcome {member.name} to Ferret\'s Palace.  Please enjoy your stay.\nKeep in mind, you will need to go to <#929353951818690660> to gain access to channels!'
        await self.welcome_log.send(f"{member.mention}")
        await self.welcome_log.send(embed=utils.SpecialEmbed(title=f"{greeting}", desc=desc, thumbnail=member.avatar_url))
        await self.members_log.send(embed=utils.LogEmbed(type=f"positive", title=f"New member joined", desc=f"Username: {member.name}\nStatus: {member.status}", thumbnail=member.avatar_url))


    #! Logs
    @Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('__________________')
        await self.bot_log.send(embed=utils.LogEmbed(type="positive", title=f"Mink! is Online!", desc=f"Ping: {math.floor(self.bot.latency*1000)}"))

    @Cog.listener()
    async def on_guild_join(self, guild):
        user_count = len(set(self.bot.get_all_members()))
        await self.bot_log.send(embed=utils.LogEmbed(type="positive", title=f"The bot has joined {guild.name}", desc=f"Bot now manages: {user_count:,} users"))
        

    @Cog.listener()
    async def on_guild_remove(self, guild):
        user_count = len(set(self.bot.get_all_members()))
        await self.bot_log.send(embed=utils.LogEmbed(type="negative", title=f"The bot has left {guild.name}", desc=f"Bot now manages: {user_count:,} users"))

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.bot_log.send(f"Command failed - `{error!s}`;")
        raise error



    #! Guild Logs
    @Cog.listener()
    async def on_member_remove(self, member):
        try:
            if member.bot: return
            await self.members_log.send(embed=utils.LogEmbed(type="negative", title=f"{member.name} has left the realm.", thumbnail=member.avatar_url))
        except: pass #? Fail Silently

    @Cog.listener()
    async def on_member_ban(self, guild, member):
        try:
            await self.members_log.send(embed=utils.LogEmbed(type="negative", title=f"Member Banned", desc=f"{member} has been banned!"))
        except: pass #? Fail Silently

    @Cog.listener()
    async def on_member_unban(self, guild, member):
        try:
            await self.members_log.send(embed=utils.LogEmbed(type="change", title=f"Member Unbanned", desc=f"{member} has been unbanned!"))
        except: pass #? Fail Silently

    @Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot: return
        if message.attachments: 
            image = message.attachments[0].url 
        else: image = None
        try:
            await self.message_log.send(embed=utils.LogEmbed(type="negative", title=f"Message Deleted", desc=f"\"{message.content}\"\n**Channel:** <#{message.channel.id}>\n**Author:** {message.author.mention}", thumbnail=message.author.avatar_url, image=image))
        except: pass #? Fail Silently

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot: return
        if before.content == after.content: return
        try:
            await self.message_log.send(embed=utils.LogEmbed(type="change", title=f"Message Edited", desc=f"**Author:** {before.author.mention}\n**Channel:** <#{before.channel.id}>\n**Before:**\n{before.content}\n\n**after:**\n{after.content}", thumbnail=before.author.avatar_url))
        except: pass #? Fail Silently

    @Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        try:
            await self.message_log.send(embed=utils.LogEmbed(type="positive", title=f"Message Pinned", desc=f"A pinned in: <#{channel.id}>\n{last_pin} was made/modify!"))
        except: pass #? Fail Silently




def setup(bot):
    x = Logging(bot)
    bot.add_cog(x)
