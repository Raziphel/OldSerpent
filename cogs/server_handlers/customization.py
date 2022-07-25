
from discord import Embed, Member, Message, RawReactionActionEvent  
from discord.ext.commands import Cog 

import utils


class Customization(Cog): #! Gonna be honest if theres a bunch of servers needing this it will get way to fucking big...  Eventually need to make an automated system able to do them all.

    def __init__(self, bot):
        self.bot = bot

    @property  #! The members logs
    def members_log(self):
        return self.bot.get_channel(self.bot.config['channels']['members_log']) #?Members log channel



    @Cog.listener()
    async def on_ready(self):
        '''Edits the Realm's role handler!'''

        ch = self.bot.get_channel(self.bot.config['channels']['role_handler'])

        msg1 = await ch.fetch_message(956840593600950292) #? Role handler messages
        msg2 = await ch.fetch_message(956840606603280424)
        msg3 = await ch.fetch_message(956840664002342952)
        msg4 = await ch.fetch_message(956840677600280586)
        msg5 = await ch.fetch_message(956840695392526397)
        msg6 = await ch.fetch_message(956840717534236712)

        embed1=Embed(title=f"**[- Pings for Bot & Server updates -]**", description=f"📕 **Get pings for __Server__ related updates / changes** 📕\n\n📗 **Get pings for __Bot__ related updates / changes** 📗\n", color=0x8f00f8)

        embed2=Embed(title=f"**[- Gain Adult Access -]**", description=f"✅ **Identify as an __adult!__ ( Gives NSFW Access)** ✅\n\n🌼 **Identify as an __adult!__ ( No NSFW Access)** 🌼\n\n❌ **Identify as __underage__.  (Its not worth lying.)** ❌", color=0x8f00f8)

        embed3=Embed(title=f"**[- Coming Soon -]**", description=f".", color=0x8f00f8)

        embed4=Embed(title=f"**[- Personal Bot Setting -]**", description=f"🎤 **Get messages about VC earnings** 🎤\n\n🔰 **Disable being able to Prestige** 🔰\n\n🎉 **Get level messages from being in VC** 🎉", color=0x8f00f8)

        embed5=Embed(title=f"**[- Coming Soon -]**", description=f".", color=0x8f00f8)

        embed6=Embed(title=f"**[- Coming Soon -]**", description=f".", color=0x8f00f8)



        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f" ", embed=embed4)
        await msg5.edit(content=f" ", embed=embed5)
        await msg6.edit(content=f" ", embed=embed6)





    @Cog.listener('on_raw_reaction_add')
    async def role_add(self, payload:RawReactionActionEvent):
        """Reaction role add handler"""

        # Validate channel
        if payload.channel_id != self.bot.config['channels']['role_handler']:
            return

        # Not bot
        if self.bot.get_user(payload.user_id).bot:
            return

        # See what the emoji is
        if payload.emoji.is_unicode_emoji():
            emoji = payload.emoji.name
        else:
            emoji = payload.emoji.id

        # Work out out cached items
        channel = self.bot.get_channel(payload.channel_id)
        guild = channel.guild
        member = guild.get_member(payload.user_id)

        # Get the right role
        role = await self.get_role(emoji=emoji, member=member, guild=guild)
        if role:
            await member.add_roles(role, reason="Role picker entry")

        # Check to see total reactions on the message
        message = await channel.fetch_message(payload.message_id)
        emoji = [i.emoji for i in message.reactions]
        if sum([i.count for i in message.reactions]) > 200:
            await message.clear_reactions()
        for e in emoji:
            await message.add_reaction(e)

    @Cog.listener('on_raw_reaction_remove')
    async def role_remove(self, payload:RawReactionActionEvent):
        """Reaction role removal handler"""

        if payload.channel_id != self.bot.config['channels']['role_handler']:
            return

        # See what the emoji is
        if payload.emoji.is_unicode_emoji():
            emoji = payload.emoji.name
        else:
            emoji = payload.emoji.id

        # Get the right role
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = await self.get_role(emoji=emoji, member=member, guild=guild)
        if role is None:
            return

        # Add to the user
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role, reason="Role picker entry")



    async def get_role(self, emoji, member, guild):
        """Gets the role given a picked emoji If the user has picked to enable mention alerts or VC messages, the bot will configure that _here_"""

        mod = utils.Moderation.get(member.id)
        ss = utils.Settings.get(member.id)
        role = None
        # Role picker emoji
        if emoji == "📕":
            role = utils.DiscordGet(guild.roles, name="Discord")
        elif emoji == "📗":
            role = utils.DiscordGet(guild.roles, name="Bot")
        elif emoji == "📘":
            role = utils.DiscordGet(guild.roles, name="Minecraft")

        elif emoji == "✅":
            if mod.child == False and mod.adult == False:
                mod.adult = True
                role = utils.DiscordGet(guild.roles, name="Adult 🚬")
                await member.add_roles(role)
                await self.members_log.send(embed=utils.LogEmbed(type="Special", title=f"Got Adult Role", desc=f"{member.name} was given Adult access!"))
        elif emoji == "🌼":
            if mod.child == False and mod.adult == False:
                mod.adult = True
                role = utils.DiscordGet(guild.roles, name="Adult 🍺")
                await member.add_roles(role)
                await self.members_log.send(embed=utils.LogEmbed(type="Special", title=f"Got Adult Role", desc=f"{member.name} was given Adult access!"))
        elif emoji == "❌":
            mod = utils.Moderation(member.id)
            mod.child = True
            mod.adult = False
            role = utils.DiscordGet(guild.roles, name="Child 🍼")



        elif emoji == "🎤":
            if ss.vc_msgs == True:
                ss.vc_msgs = False
                await member.send(embed=utils.DefualtEmbed(title="Setting has been changed", desc=f"You will no longer recieve messages about earning you make in vc!"))
            elif ss.vc_msgs == False:
                ss.vc_msgs = True
                await member.send(embed=utils.DefualtEmbed(title="Setting has been changed", desc=f"You will now recieve messages about earning you make in vc!"))

        elif emoji == "🔰":
            #! Need to set that up eventually
            return

        elif emoji == "⛏":
            if ss.vc_lvls == True:
                ss.vc_lvls = False
                await member.send(embed=utils.DefualtEmbed(title="Setting has been changed", desc=f"You will no longer recieve messages about leveling up in vc!"))
            elif ss.vc_lvls == False:
                ss.vc_lvls = True
                await member.send(embed=utils.DefualtEmbed(title="Setting has been changed", desc=f"You will now recieve messages about leveling up in vc!"))


        if role:
            return role

        async with self.bot.database() as db:
            await mod.save(db)
            await ss.save(db)


def setup(bot):
    x = Customization(bot)
    bot.add_cog(x)
