
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
        ch = guild.get_channel(self.bot.config['channels']['server']) #? Rules Channel

        rules1 = await ch.fetch_message(956470547426996244) #? 
        rules2 = await ch.fetch_message(956470556415361024) #? 
        rules3 = await ch.fetch_message(956470560097988649) #? 
        rules4 = await ch.fetch_message(956470570340450375) #? 
        rules5 = await ch.fetch_message(956470575411388436) #? 

        embed1=Embed(title=f"**[- The Server's Rules -]**", 
        description=f"**These are rules for the entire Discord Server.**\n\n**1.)** Respect Everyone, not a single person doesn't deserve respect, especially the 05 Council.\n\n**2.)** Harrassment, Bully, Attacking of any kind or form of any member on this server isnt allowed. Period.\n\n**3.)** Drama, most people here have already gone through highschool, don't bring it back.\n\n**4.)** This server only allows the use of English.  We can not moderate other languages.\n\n**5.)** Common Sense, Don't be annoying or do anything that would make a 05 Council have to punish. (Should be easy.)\n\n**6.)** Discord TOS, obviously don't do anything discord already doesn't allow, could count as previous rule.\n\n**7.)** Accepting the chaos and rules presented by The Serpent.", color=0xF54747)

        embed2=Embed(title=f"**[- The Serpent's Game -]**", 
        description=f"**This is a list of useful information for the Serpent's Game.**\n\n**1.)** To move between areas you must use <#997346872622596136>!\n\n**2.)** Interactions with The Serpent, sending messages and being in VC will all level you up!\n\n**3.)** Getting a better role requires higher levels.\n\n**4.)** The 05 Council must use Alpha-1 to participate in my game.\n\n**5.)** When you die in my game you are made a civilian for a few hours, this could be considered the *most* general area.  Leaving open your role slot.\n\n**6.)** The Serpent's Hand can veiw the Serpent's server's logs...\n\n**7.)** For in depth information go to <#1020959150890565703>", color=0x47F599)

        embed3=Embed(title=f"**[- The 05 Council -]**", 
        description=f"The 05 Council is the Discord Server's form of Staff.  They are the only Role on the server that are **Omni-Present**. (meaning they do not have to travel between zones)\n\n**The 05 are also not allowed to interact with The Serpent like regular users.**\n\nThe \"Red Right Hand\" Alpha-1 use The Serpent normally, being the 05's only way for presence in the Serpent's Game.\n\nThe 05 Council's corresponding number is in order of rank.", color=0xF5AE47)

        embed4=Embed(title=f"**[- Moderation System -]**", 
        description=f"**By absolutely no means do the 05 Council (Staff) have to be \"Fair\", in any situation or decision. They are put there for a reason and we usually run everything past one another.**\n\nFor most situations a Council member will give a single warning and after that you are completely fair game; from that council member or any other for whatever punishment that believe you deserve.  Lying about your age, breaking Discord TOS sending spam, hate, phishing links or scamming in anyway is awlays going to be a insta-ban with no warning.  *It will not be tolerated at all.*", color=0xB6F547)

        embed5=Embed(title=f"**[- The Serpent -]**", 
        description=f"*The Serpent is the Discord bot used to play the Serpent's game*\n\nIt uses the prefix `.` and doesn't like slash commands!  It is quite important you have your settings set up where you can recieve private message from the Serpent! \n\n~~The Serpent's Hand and The Serpent might have a connection.~~", color=0x89F547)


        await rules1.edit(content=f" ", embed=embed1)
        await rules2.edit(content=f" ", embed=embed2)
        await rules3.edit(content=f" ", embed=embed3)
        await rules4.edit(content=f" ", embed=embed4)
        await rules5.edit(content=f" ", embed=embed5)





    @Cog.listener('on_ready')
    async def verify_msg(self):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['zones']) #? Rules Channel

        msg1 = await ch.fetch_message(1011068499495497748) #? msg
        msg2 = await ch.fetch_message(1011068510320992325) #? msg
        msg3 = await ch.fetch_message(1011068526028660787) #? msg

        embed1=Embed(title=f"**[- Redacted Areas -]**", 
        description=f"📯 **__Site-01__**\n> Spawn location for **05 Council**\n> Spawn location for **The Red Hand**\n> Access to the very powerful <#1021645303805390928>\n`Only accessible from Civilian Area`\n\n🐍 **__Wander's Library__**\n> Spawn location for **The Serpent's Hand**\n> Access to all the **Server's & Bot's Logs**\n> Access to the <#1021172170178711563> which gives important information going on in the game\n`Only accessible from Out-Skirts with a Serpent's Ring`\n\n💣 **__Chaotic Bases__**\n> Spawn location for **Chaos Insurgency**\n> Access to the <#1021664074469212220> with illegal items for sale.\n`Only accessible from The out-skirts`", color=0xFF0000)

        embed2=Embed(title=f"**[- Outside Areas -]**", 
        description=f"\n🎭 **__Civilian Areas__**\n> Spawn location for **Civilian**\n> A safe area for all roles\n`Only accessible from Redacted Areas and in any Entrance Zone`\n\n🌲 **__Out-Skirts__**\n> A total anarchy zone\n`Only accessible from Wander's Library, Chaos Base and any Site Entrance`", color=0x0000FF)

        embed3=Embed(title=f"**[- Site 02 -]**", 
        description=f"⛳ **__Site-02 Surface__**\n> Spawn location for **Facility Guard**\n> Access to the <#1022379864449351731> capable of destroying Site-02\n`Only accessible from Outside Areas with a Level 4 keycard`\n\n🚪 **__Entrance Zone__**\n> Spawn location for **Scientist, Facility Guard**\n> Has tasks in <#1021239810045771786> for containment Engineers\n> Has tasks in <#1021231813647147038> for scientists\n`Only accessible from Surface or Heavy with a Level 2 Keycard`\n\n🔒 **__Heavy Zone__**\n> Access to the <#1021203903561338930> which has controls to Site-02\n> Access to the <#1020935245589119007> which has stocks of weapons\n`Only accessible from Entrance Zone or Light with a Level 2 Keyard`\n\n⛓ **__Light Zone__**\n> Access to the <#807829051607351296> which has memes and jobs for scientists\n> Capable of using **SCP-914** with a **level 2** Key Card\n`Only accessible from Heavy with a Level 2 Keyard`", color=0xFFFFFF)

        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)









    @Cog.listener('on_ready')
    async def verify_msg(self):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['rules']) #? Rules Channel

        table = await ch.fetch_message(1021285665373163530) #? msg intro
        msg1 = await ch.fetch_message(1021285478210748428) #? msg 1
        msg2 = await ch.fetch_message(1021285487815700500) #? msg 2
        msg3 = await ch.fetch_message(1021285495268982794) #? msg 3

        embed1=Embed(title=f"**[- Table of Contents -]**", 
        description=f"Welcome to the Serpent's Game, this channel catalogs any and all the information relating to the entire Serpent's Garden.\n\n[1. Intro](https://discord.com/channels/689534383878701223/1020959150890565703/1021285478210748428)\n[2. The Faction Roles](https://discord.com/channels/689534383878701223/1020959150890565703/1021285487815700500)\n[3. The Foundation Roles](https://discord.com/channels/689534383878701223/1020959150890565703/1021285495268982794)", color=0xFF0000)

        embed2=Embed(title=f"**[- 1. Intro (NEW) -]**", 
        description=f"**Welcome to the Serpent's game!**\n\nFor starters the goal in development is to keep the game as simplistic as possible and be more a fun different Discord expierence.\nThere is currently no win conditions in the game at this time, this is planned to be changed some day.\n\n Reading throught this Handbook will be the 1 spot \"wikipedia\" for the entire game and how most things function!\nLook for the flairs in the titles such as (New or Changed) to find updates.", color=0x0000FF)

        embed3=Embed(title=f"**[- 2. The Faction Roles (NEW) -]**", 
        description=f"**Here is a list of all the current roles outside of the Foundation; along with information about each and how they play!**\n\n<:foundation:1024847941665562634> **__The 05 Council__**\nThe 05 Council, known for being the Head leaders of the Foundation, play as staff role for the server, that players can not obtain unless accepted via application.  This is the only class that has Omni-Presense being able to see every zone and area, but not being able to partipate in the game beyone using the Red Hand or things located in Site-01.\n\n<:KETER:1020576689245392937> **__SCPs__**\nThese are the driving forces of everything.  In The Serpent's Game some of these are not played by players.  But the ones that are played by players will be the most deadly!  Sadly dying in this role, only re-contains the SCP.\n\n🐍 **__Serpent's Hand__**\nSupporting force for the SCPs and an enemy to The Foundation!  Has access to the Wander's Library giving them the information advatage with access to the server logs. (Also viewable by 05, ofcourse.)  I, The Serpent could be considered the leader of this faction and give the orders.\n\n💣 **__The Chaos Insurgency__**\nAnother enemy to the Foundation, but not for the SCP's sake!  This spliter faction from the foundation now seeks out its anomalies for there purposes.  Constantly wanting to recruit anyone whos been involved with the foundation; for use as forces against the founation!", color=0x00FF00)

        embed4=Embed(title=f"**[- 3. The Foundation Roles (NEW) -]**", 
        description=f"**Here is a list of all the current foundation roles; along with information about each and how they play!**\n\n<:RedRightHand:1020893683853303828> **__Red Right Hand__**\nAka. Alpha-01 is known as being the Elite guard under the 05 Council and it carries over in the Serpent's game!  The Red right hand are to do orders given by the 05 Council, being the 05 Council's main way of participating in the game.\n\n🥽 **__Mobile Task Force__**\nThe special task froce sent between facilities to take control of any situations that get out of control.  Primarily ordered by Facility managers to handle specific situations; however 05 Council could use them if situations arised to the location.\n\n🔑 **__Facility Managers__**\nAs the managers of the facility you have the highest card access of Level 4.", color=0x00FFF0)

        await table.edit(content=f" ", embed=embed1)
        await msg1.edit(content=f" ", embed=embed2)
        await msg2.edit(content=f" ", embed=embed3)
        await msg3.edit(content=f" ", embed=embed4)


























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