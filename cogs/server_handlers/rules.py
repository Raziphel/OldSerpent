
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





    @Cog.listener('on_ready')
    async def rules_msg(self):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['rules']) #? Rules Channel

        rules1 = await ch.fetch_message(956470547426996244) #? 
        rules2 = await ch.fetch_message(956470556415361024) #? 
        rules3 = await ch.fetch_message(956470560097988649) #? 
        rules4 = await ch.fetch_message(956470570340450375) #? 
        rules5 = await ch.fetch_message(956470575411388436) #? 

        embed1=Embed(title=f"**[- The Ferret's Rules -]**", 
        description=f"**This is probably important by the way!**\n\n**1.)** Respect Everyone, not a single person doesn't deserve respect, especially the Council.\n\n**2.)** Harrassment, Bully, Attacking of any kind or form of any member on this server isnt allowed. Period.\n\n**3.)** Drama, most people here have already gone through highschool, don't bring it back.\n\n**4.)** ENGLISH.  This is an American server you will be expected to only speak english or not speak at all.\n\n**5.)** Common Sense, Don't be annoying or do anything that would make a council have to punish. (Should be easy.)\n\n**6.)** Discord TOS, obviously don't do anything discord already doesn't allow, could count as previous rule.\n\n**7.)** Exploitation of any form with our bots or using your own is not allowed.", color=0x1d89e3)

        embed2=Embed(title=f"**[- The Council -]**", 
        description=f"The server council are the only form of staff that this server has.  They make every decision and give out every punishment.  They are numbered in a list of power, but all possess the same voting power when it comes to major decisions. Here they are: (In order of power)\n\n**1.)** <@159516156728836097>\n**2.)** <@204365008484827136>\n**3.)** <@203660218863845376>\n**4.)** <@773327148764102706>\n**5.) <@335978305033469956>**\n**6.)** <@202810961407639552>\n**7.)** <@513463757385760768>\n**8.) <@601271225263849482>** ", color=0x1d89e3)

        embed3=Embed(title=f"**[- The Punishment System -]**", 
        description=f"**By absolutely no means do the Council have to be \"Fair\", in any situation or decision. They are put there for a reason and we usually run everything past one another.**\n\nFor most situations a Council member will give a single warning and after that you are completely fair game; from that council member or any other for whatever punishment that believe you deserve.  Lying about your age, breaking Discord TOS sending spam, hate, phishing links or scamming in anyway is awlays going to be a insta-ban with no warning.  *It will not be tolerated at all.*", color=0x1d89e3)

        embed4=Embed(title=f"**[- The Holy Mink -]**", 
        description=f"*The Bot generating this text your reading right now, is soley coded and maintained by Council 01.*\n\nI, The Mink does practically everything for this server!  It is quite important you have your settings set up where you can recieve dms from me.  It would also be very foolish to block me; if ya plan on using this server atleast.", color=0x1d89e3)

        embed5=Embed(title=f"**[- Enjoy -]**", 
        description=f"*Please enjoy your stay in this Ferret Cult. The Mink and The Council welcome you.*", color=0x1d89e3)

        await rules1.edit(content=f" ", embed=embed1)
        await rules2.edit(content=f" ", embed=embed2)
        await rules3.edit(content=f" ", embed=embed3)
        await rules4.edit(content=f" ", embed=embed4)
        await rules5.edit(content=f" ", embed=embed5)





    @Cog.listener('on_ready')
    async def verify_msg(self):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['verify']) #? Rules Channel

        msg = await ch.fetch_message(997347478020038716) #? msg

        embed1=Embed(title=f"**[- Welcome to the Server! -]**", 
        description=f"**This server does require verification, make sure the bot can message you and click the reactions you are wanting access to!**\n\n🎀 `General Server Verification`\n🏹 `Grepolis Alliance Verification`", color=0x1d89e3)


        await msg.edit(content=f" ", embed=embed1)



    @Cog.listener('on_raw_reaction_add')
    async def role_add(self, payload:RawReactionActionEvent):
        """Reaction role add handler"""

        # Validate channel
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

        # Get the right verification
        if emoji == "🎀":
            await self.bot.get_cog('Verification').verification(author=member, guild=guild)
        elif emoji == "🏹":
            await self.bot.get_cog('Verification').verify_kingussy(author=member, guild=guild)

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