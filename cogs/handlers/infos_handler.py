
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

class rules_handler(Cog):
    def __init__(self, bot):
        self.bot = bot


    @property  #! The members logs
    def members_log(self):
        return self.bot.get_channel(self.bot.config['channels']['members_log']) 


    @Cog.listener('on_ready')
    async def rules_msg(self):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['rules']) #? Rules Channel

        rules1 = await ch.fetch_message(956470547426996244) #? 
        rules2 = await ch.fetch_message(956470556415361024) #? 
        rules3 = await ch.fetch_message(956470560097988649) #? 
        rules4 = await ch.fetch_message(956470570340450375) #? 
        rules5 = await ch.fetch_message(956470575411388436) #? 

        embed1=Embed(title=f"**[- The Server's Rules -]**", 
        description=f"**This is probably important by the way!**\n\n**1.)** Respect Everyone, not a single person doesn't deserve respect, especially the Council.\n\n**2.)** Harrassment, Bully, Attacking of any kind or form of any member on this server isnt allowed. Period.\n\n**3.)** Drama, most people here have already gone through highschool, don't bring it back.\n\n**4.)** ENGLISH.  This is an American server you will be expected to only speak english or not speak at all.\n\n**5.)** Common Sense, Don't be annoying or do anything that would make a council have to punish. (Should be easy.)\n\n**6.)** Discord TOS, obviously don't do anything discord already doesn't allow, could count as previous rule.\n\n**7.)** Exploitation of any form with our bots or using your own is not allowed.", color=0xF54747)

        embed2=Embed(title=f"**[- The 05 Council -]**", 
        description=f"The server council are the only form of staff that this server has.  They make every decision and give out every punishment.  They are numbered in a list of power, but all possess the same voting power when it comes to major decisions. (In order of power)\n\n**1.)** <@159516156728836097>\n**2.)** <@204365008484827136>\n**3.)** <@203660218863845376>\n**4.)** <@773327148764102706>\n**5.) <@335978305033469956>**\n**6.) <@513463757385760768>**\n**7.) <@202810961407639552>**\n**8.)** ", color=0xF5AE47)

        embed3=Embed(title=f"**[- The Punishment System -]**", 
        description=f"**By absolutely no means do the Council have to be \"Fair\", in any situation or decision. They are put there for a reason and we usually run everything past one another.**\n\nFor most situations a Council member will give a single warning and after that you are completely fair game; from that council member or any other for whatever punishment that believe you deserve.  Lying about your age, breaking Discord TOS sending spam, hate, phishing links or scamming in anyway is awlays going to be a insta-ban with no warning.  *It will not be tolerated at all.*", color=0xB6F547)

        embed4=Embed(title=f"**[- Serphent's Hand -]**", 
        description=f"*The Bot generating this text your reading right now, is soley coded and maintained by Council 01.*\n\nI do practically everything for this server!  It is quite important you have your settings set up where you can recieve dms from me.  It would also be very dumb to block me; if ya plan on using this server atleast.", color=0x89F547)

        embed5=Embed(title=f"**[- Logging -]**", 
        description=f"To make the server more transparent and to allow more moderation help.  The __server logs__ are capable of being viewed by anyone!  This can be used to see almost every interaction from the bot or the discord server, even editing messages.  So keep in mind that any user can view any and all actions done.", color=0x47F599)

        await rules1.edit(content=f" ", embed=embed1)
        await rules2.edit(content=f" ", embed=embed2)
        await rules3.edit(content=f" ", embed=embed3)
        await rules4.edit(content=f" ", embed=embed4)
        await rules5.edit(content=f" ", embed=embed5)





    @Cog.listener('on_ready')
    async def verify_msg(self):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['verify']) #? Rules Channel

        msg1 = await ch.fetch_message(1011068499495497748) #? msg
        msg2 = await ch.fetch_message(1011068510320992325) #? msg
        msg3 = await ch.fetch_message(1011068526028660787) #? msg

        embed1=Embed(title=f"**[- Primary Channel Access -]**", 
        description=f"**Razi's Realm has multiple different sections to it!**\nYou may not want access to all these different sections.  So you can simply choose what you would like to have access to, using this handler!\n\n*Channels have very different permissions (Ex: Posting Images) depending on what they're about.*\n\n**These are channels more related to Razi, could be the server's main channels!**\n\n*( You will have to agree to rules in verification. )*\n🎀 `Razi's Lounge`\n❧ This gives you access to Razi's General channels!\n❧ Permissions require <#946730953731100682> purchases.\n\n📚 `Wander's Library`\n❧ This gives you access to all of the Server's Logs.\n❧ Channels are read only and Adult Logs only visible by adults.\n**Now requires purchase from <#946730953731100682>**.", color=0x47D0F5)

        embed2=Embed(title=f"**[- Secondary Channel Access -]**", 
        description=f"*(You will have to be accepted by the council via verification)*\n🏹 `Kingussy Brothers`\n❧ This is for those who apart of the Kingussy alliance!\n❧ This requires a password only Ussy brothers would know.\n\n🧸 `SCP Fanatic`\n❧ This is for the SCP fanatics.\n❧ Has information for the *SCP:Secret Labratory* server information.\n❧ Permissions require <#946730953731100682> purchases.\n❧ Doesn't require verification.\n\n🐾 `Furry`\n❧ This is for the people into furry art and hangin' with other furfags.\n❧ No RP/ERP.\n❧ No flirting/dating.\n❧ No being a cringe lord.", color=0x4799F5)

        embed3=Embed(title=f"**[- Age Verification -]**", 
        description=f"**To gain access to any above sections NSFW channels, you will have to pass verification.  It will have requirements.**\n\n*(You will have to be accepted by the council via verification)*\n🔥 `Adult Verification`\n❧ Gives NSFW access for any section you are apart of.\n\n💦 `Kinda Adult Verification`\n❧ Marked as Adult but no NSFW text/image channel access.\n\n🎈 `Underage`\n❧ Marks you as a child and keeps you safe!\n❧ Lying about your age never pays off.", color=0xD047F5)

        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)



    @Cog.listener('on_raw_reaction_add')
    async def role_add(self, payload:RawReactionActionEvent):
        """Reaction role add handler"""

        #* Validate channel
        if payload.channel_id != self.bot.config['channels']['verify']:
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
        mod = utils.Moderation.get(member.id)

        # Get the right verification
        if emoji == "🎀":
            await self.bot.get_cog('Verification').verification(author=member, guild=guild)
        elif emoji == "🏹":
            await self.bot.get_cog('Verification').verify_kingussy(author=member, guild=guild)
        elif emoji == "🐾":
            await self.bot.get_cog('Verification').verify_furry(author=member, guild=guild)
        elif emoji == "🧸":
            scp = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['scp'])
            await member.add_roles(scp, reason="SCP Access Granted.")
        elif emoji == "🔥":
            if mod.child == False:
                await self.bot.get_cog('Verification').verify_adult(author=member, guild=guild)
        elif emoji == "💦":
            if mod.child == False:
                await self.bot.get_cog('Verification').verify_adult(author=member, guild=guild, kinda=True)
        elif emoji == "🎈":
            mod.child = True
            child = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['child'])
            await member.add_roles(child, reason="Marked as child.")

        async with self.bot.database() as db:
            await mod.save(db)


        # Check to see total reactions on the message
        message = await channel.fetch_message(payload.message_id)
        emoji = [i.emoji for i in message.reactions]
        if sum([i.count for i in message.reactions]) > 200:
            await message.clear_reactions()
        for e in emoji:
            await message.add_reaction(e)




def setup(bot):
    x = rules_handler(bot)
    bot.add_cog(x)