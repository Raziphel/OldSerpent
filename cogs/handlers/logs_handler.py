
#* Discord
from discord.ext.commands import Cog
#* Additions
import math

import utils
# * Additions
import math

from discord.ext.commands import Cog

import utils


class Logging(Cog):

    def __init__(self, bot):
        self.bot = bot

    @property  #! The Server logs
    def bot_log(self):
        return self.bot.get_channel(self.bot.config['channels']['bot']) 

    @property  #! The members logs
    def discord_log(self):
        return self.bot.get_channel(self.bot.config['channels']['server']) 

    @property  #! The message logs
    def message_log(self):
        return self.bot.get_channel(self.bot.config['channels']['messages']) 

    @property  #! The welcome logs
    def welcome_log(self):
        return self.bot.get_channel(self.bot.config['channels']['welcome'])

    @property  #! The adult logs
    def adult_log(self):
        return self.bot.get_channel(self.bot.config['channels']['adult'])

    @property  #! The adult logs
    def staff_log(self):
        return self.bot.get_channel(1070960923587645481)



    #! Welcome channel 
    @Cog.listener()
    async def on_member_join(self, member):
        await utils.UserFunction.verify_user(user=member, type='guild')
        await utils.UserFunction.check_level(user=member)
        await self.discord_log.send(embed=utils.LogEmbed(type="positive", title=f"{member.name} has entered the Garden.", thumbnail=member.avatar.url))


    #! Logs
    @Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('__________________')
        if math.floor(self.bot.latency*1000) <= 100: #? Secret bullshit bro.
            await self.bot_log.send(embed=utils.LogEmbed(type="positive", title=f"Serpent is Online!", desc=f"Perfect Restart."))
        elif math.floor(self.bot.latency*1000) <= 420:
            await self.bot_log.send(embed=utils.LogEmbed(type="change", title=f"Serpent is Online!", desc=f"Weird Restart."))
        elif math.floor(self.bot.latency*1000) > 200:
            await self.bot_log.send(embed=utils.LogEmbed(type="change", title=f"Serpent is Online!", desc=f"Discord Connection Refresh"))


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
            await self.discord_log.send(embed=utils.LogEmbed(type="negative", title=f"{member.name} has left the Garden.", thumbnail=member.avatar.url))
            # c = utils.Currency.get(member.id)
            # lvl = utils.Level.get(member.id)
            # lvl.level = 0
            # c.coins = 0
            # async with self.bot.database() as db:
            #     await c.save(db)
            #     await lvl.save(db)
        except: pass #? Fail Silently



    @Cog.listener()
    async def on_member_ban(self, guild, member):
        try:
            await self.discord_log.send(embed=utils.LogEmbed(type="negative", title=f"Member Banned", desc=f"{member} has been banned!"))
        except: pass #? Fail Silently

    @Cog.listener()
    async def on_member_unban(self, guild, member):
        try:
            await self.discord_log.send(embed=utils.LogEmbed(type="change", title=f"Member Unbanned", desc=f"{member} has been unbanned!"))
        except: pass #? Fail Silently

    @Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot: return
        image = None
        if message is None:
            return
        if message.channel.name is None:
            return
        if message.attachments: 
            image = message.attachments[0].url 
        name_list = list(message.channel.name)

        if any(item in name_list for item in ['🔥', "✨"]):
            channel = self.staff_log
        elif any(item in name_list for item in ['👑', "🌷", "📯", "📝"]):
            return
        else: channel = self.message_log
        await channel.send(embed=utils.LogEmbed(type="negative", title=f"Message Deleted", desc=f"\"{message.content}\"\n**Channel:** <#{message.channel.id}>\n**Author:** {message.author.mention}", thumbnail=message.author.avatar.url, image=image))

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot: return
        if before.content == after.content: return
        name_list = list(before.channel.name)

        if any(item in name_list for item in ['🔥', "✨"]):
            channel = self.staff_log
        elif any(item in name_list for item in ['👑', "🌷", "📯", "📝"]):
            return
        else: channel = self.message_log
        await channel.send(embed=utils.LogEmbed(type="change", title=f"Message Edited", desc=f"**Author:** {before.author.mention}\n**Channel:** <#{before.channel.id}>\n**Before:**\n{before.content}\n\n**after:**\n{after.content}", thumbnail=before.author.avatar.url))

    @Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        try:
            await self.message_log.send(embed=utils.LogEmbed(type="positive", title=f"Message Pinned", desc=f"A pinned in: <#{channel.id}>\n{last_pin} was made/modify!"))
        except: pass #? Fail Silently





def setup(bot):
    x = Logging(bot)
    bot.add_cog(x)
