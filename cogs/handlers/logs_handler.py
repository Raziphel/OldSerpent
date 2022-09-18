
#* Discord
from discord.ext.commands import command, Cog
from discord.utils import get
#* Additions
import math
from random import randint, choice

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

    @property  #! The adult logs
    def adult_log(self):
        return self.bot.get_channel(self.bot.config['channels']['adult_log'])



    #! Welcome channel 
    @Cog.listener()
    async def on_member_join(self, member):
        if self.welcome_log == None: return #! Fail silently
        desc = f'__**Welcome {member.name} to Razi\'s Anomalies**__\nPlease read the rules channel, Its practically a wiki of information!\n*Enjoy your stay~*'
        await self.welcome_log.send(f"{member.mention}")
        await self.welcome_log.send(embed=utils.SpecialEmbed(title=f"Welcome new D-Class Personel", desc=desc, thumbnail=member.avatar.url))
        await self.members_log.send(embed=utils.LogEmbed(type=f"positive", title=f"New member joined", desc=f"Username: {member.name}\nStatus: {member.status}", thumbnail=member.avatar.url))


    #! Logs
    @Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('__________________')
        await self.bot_log.send(embed=utils.LogEmbed(type="positive", title=f"Serpent is Online!", desc=f"Ping: {math.floor(self.bot.latency*1000)}"))

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
            await self.members_log.send(embed=utils.LogEmbed(type="negative", title=f"{member.name} has left the realm.", thumbnail=member.avatar.url))
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
        image = None
        if message.attachments: 
            image = message.attachments[0].url 
        if message.channel.is_nsfw():
            channel = self.adult_log
        else: channel = self.message_log
        await channel.send(embed=utils.LogEmbed(type="negative", title=f"Message Deleted", desc=f"\"{message.content}\"\n**Channel:** <#{message.channel.id}>\n**Author:** {message.author.mention}", thumbnail=message.author.avatar.url, image=image))

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot: return
        if before.content == after.content: return
        if before.channel.is_nsfw():
            channel = self.adult_log
        else: channel = self.message_log
        await channel.send(embed=utils.LogEmbed(type="change", title=f"Message Edited", desc=f"**Author:** {before.author.mention}\n**Channel:** <#{before.channel.id}>\n**Before:**\n{before.content}\n\n**after:**\n{after.content}", thumbnail=before.author.avatar.url))

    @Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        try:
            await self.message_log.send(embed=utils.LogEmbed(type="positive", title=f"Message Pinned", desc=f"A pinned in: <#{channel.id}>\n{last_pin} was made/modify!"))
        except: pass #? Fail Silently

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since is None and after.premium_since is not None:
            c = utils.Currency(before.author.id)
            try:
                await user.send(embed=utils.SpecialEmbed(title="- Nitro Booster Coin Reward -", desc=f"A small reward for being a nitro booster!\n\n**+500 {goldcoin}**\n**+5 {goodcoin}**\n**+5 {evilcoin}**", footer=f"You can expect this reward every 30 days!"))
            except: pass
            c.coins += 500
            c.good_coins += 25
            c.evil_coins += 1
            for user in guild.members:
                if nitro in user.roles:
                    c = utils.Currency(user.id)
                    try:
                        await user.send(embed=utils.SpecialEmbed(title="- Nitro Booster Coin Reward -", desc=f"A small reward becuase someone nitro boosted!\n\n**+500 {goldcoin}**\n**+5 {goodcoin}**\n**+5 {evilcoin}**", footer=f"You can expect this reward every time someone boosts!"))
                    except: pass
                    c.coins += 100
                    c.good_coins += 10
                    c.evil_coins += 0
                    async with self.bot.database() as db:
                        await c.save(db)
                    print('Handed out Boost rewards')



def setup(bot):
    x = Logging(bot)
    bot.add_cog(x)
