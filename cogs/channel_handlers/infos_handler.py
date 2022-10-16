
#* Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter
from discord import Member, Message, User, TextChannel, Role, RawReactionActionEvent, Embed
import utils
#* Additions
from asyncio import iscoroutine, gather, sleep
from traceback import format_exc
from math import floor
from random import randint, choice
from datetime import datetime as dt, timedelta

import utils

class rules_handler(Cog):
    def __init__(self, bot):
        self.bot = bot



    @Cog.listener('on_ready')
    async def rules(self):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['rules']) #? Rules Channel

        rules1 = await ch.fetch_message(956470547426996244) #? 
        rules2 = await ch.fetch_message(956470556415361024) #? 
        rules3 = await ch.fetch_message(956470560097988649) #? 
        rules4 = await ch.fetch_message(956470570340450375) #? 
        rules5 = await ch.fetch_message(956470575411388436) #? 

        embed1=Embed(title=f"**[- The Server's Rules -]**", 
        description=f"**These are rules for the entire Discord Server.**\n\n**1.)** Respect Everyone, not a single person doesn't deserve respect, especially the 05 Council.\n\n**2.)** Harrassment, Bully, Attacking of any kind or form of any member on this server isnt allowed. Period.\n\n**3.)** Drama, most people here have already gone through highschool, don't bring it back.\n\n**4.)** This server only allows the use of English.  We can not moderate other languages.\n\n**5.)** Common Sense, Don't be annoying or do anything that would make a 05 Council have to punish. (Should be easy.)\n\n**6.)** Discord TOS, obviously don't do anything discord already doesn't allow, could count as previous rule.\n\n**7.)** Accepting the chaos and rules presented by The Serpent.", color=0xF54747)

        embed2=Embed(title=f"**[- The Serpent's Game -]**", 
        description=f"**This is a list of useful information for the Serpent's Game.**\n\n**1.)** To move between areas you must use <#1021288155040714782>!\n\n**2.)** Interactions with The Serpent, doing tasks, sending messages and being in VC will all give you xp and coins!\n\n**3.)** Getting a better role requires higher levels.\n\n**4.)** The 05 Council must use Alpha-1 to participate in my game.\n\n**5.)** When you die in my game you are made a D-Class for a few hours, making Light Contain. the most general place.  Leaving open your role slot.\n\n**6.)** The Serpent's Hand can veiw the Serpent's server's logs...\n\n**7.)** For in depth information go to <#1020959150890565703>", color=0x47F599)

        embed3=Embed(title=f"**[- The 05 Council -]**", 
        description=f"The 05 Council is the Discord Server's form of Staff.  They are the only Role on the server that are **Omni-Present**. (meaning they do not have to travel between zones)\n\n**The 05 are also not allowed to interact with The Serpent like regular users.**\n\nThe \"Red Right Hand\" Alpha-1 use The Serpent normally, being the 05's only way for presence in the Serpent's Game.\n\nThe 05 Council's corresponding number is in order of rank.", color=0xF5AE47)

        embed4=Embed(title=f"**[- Moderation System -]**", 
        description=f"**By absolutely no means do the 05 Council (Staff) have to be \"Fair\", in any situation or decision. They are put there for a reason and we usually run everything past one another.**\n\nFor most situations a Council member will give a single warning and after that you are completely fair game; from that council member or any other for whatever punishment they believe you deserve.  Lying about your age, breaking Discord TOS, sending spam, hate, phishing links or scamming in anyway, is awlays going to be a ban with no warning.  *It won't be tolerated at all.*", color=0xB6F547)

        embed5=Embed(title=f"**[- The Serpent -]**", 
        description=f"*The Serpent is the Discord bot used to play the Serpent's game*\n\nIt uses the prefix `.` and doesn't like slash commands!  It is quite important you have your settings set up where you can recieve private message from the Serpent! \n\n~~The Serpent's Hand and The Serpent might have a connection.~~", color=0x89F547)


        await rules1.edit(content=f" ", embed=embed1)
        await rules2.edit(content=f" ", embed=embed2)
        await rules3.edit(content=f" ", embed=embed3)
        await rules4.edit(content=f" ", embed=embed4)
        await rules5.edit(content=f" ", embed=embed5)





    @Cog.listener('on_ready')
    async def role_change(self):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['role_change']) #? role change Channel

        msg1 = await ch.fetch_message(1029973755428093986) #? msg
        msg2 = await ch.fetch_message(1029973761673408543) #? msg
        msg3 = await ch.fetch_message(1029973773656531015) #? msg
        msg4 = await ch.fetch_message(1029975810251169873) #? msg
        
        coin = self.bot.config['emotes']['coin']

        embed1=Embed(title=f"**[- Permenant Roles -]**", 
        description=f"**These roles cannot and will not be taken away you from the Serpent's Game**\n\n🚬 `Adult`\nThis will give you access to any NSFW marked channels in any category on the server.  Your other roles automatically update to adult versions.\n\n🍺 `Adult?`\nThis will give you access to VC channels that only Adults can join.\nYou will not have access to the NSFW text channels.\n\n🍼 `Child`\nThis will let the mark you as a child.\nIt is encouraged to get and not lie.\n\n🐾 `Furry`\nThis role is for those degenerates!\n\n💣 `Serpent's Laboratory`\nIf you enjoy the SCP Laboratory servers be sure to get this role!\n\n🏹 `Kingussy`\nThis is for certian specific people.  You must be invited and have a password.", color=0xFF0000)

        embed2=Embed(title=f"**[- Groups of Intrest Roles -]**", 
        description=f"**These roles you must pay for to change and you are only able to change if a D-Class.** (These are the more valuable roles that suck to lose)\n\n<:KETER:1020576689245392937> **__SCPs__**\nWait for your chance to breach containment.  Get coins and xp from killing other roles.\n**[ {coin} : 500,000x ]\n[ *XP* : 10,000x ]**\n\n\n🐍 **__Serpent's Hand__**\nBreak in to the facility and help the scps.  Get coins and xp from stealing SCPs and helping scps.\n**[ {coin} : 300,000x ]\n[ *XP* : 7,500x ]**\n\n\n💣 **__The Chaos Insurgency__**\nSteal Scps and kill foundation staff during breaches.  Get coins and xp from killing other roles and stealing Scps.\n**[ {coin} : 250,000x ]\n[ *XP* : 7,500x ]**\n\n\n<:RedRightHand:1020893683853303828> **__Red Right Hand__**\nFollow all the 05's commands.  Get coins and xp directly from the 05.\n**[ {coin} : 200,000x ]\n[ *XP* : 5,000x ]**\n", color=0x0000FF)

        embed3=Embed(title=f"**[- Foundation Roles -]**", 
        description=f"**These roles you must pay for to change and you are only able to change if a D-Class.** (If you died, you become a D-Class)\n\n", color=0xFFFFFF)

        embed4=Embed(title=f"**[- Zone Changes -]**", 
        description=f"**These roles are considered locations, you must lose your current role to go to another one.** (05 Council can see every Channel.)\n\n", color=0xFF00FF)

        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f" ", embed=embed4)









    @Cog.listener('on_ready')
    async def handbook(self):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['handbook']) #? Rules Channel

        table = await ch.fetch_message(1021285665373163530) #? msg intro
        msg1 = await ch.fetch_message(1021285478210748428) #? msg 1
        msg2 = await ch.fetch_message(1021285487815700500) #? msg 2
        msg3 = await ch.fetch_message(1021285495268982794) #? msg 3
        msg4 = await ch.fetch_message(1021285508359401492) #? msg 4

        embed1=Embed(title=f"**[- Table of Contents -]**", 
        description=f"Welcome to the Serpent's Game, this channel catalogs any and all the information relating to the entire Serpent's Garden.\n\n[1. Intro](https://discord.com/channels/689534383878701223/1020959150890565703/1021285478210748428)\n[2. The Faction Roles](https://discord.com/channels/689534383878701223/1020959150890565703/1021285487815700500)\n[3. The Foundation Roles](https://discord.com/channels/689534383878701223/1020959150890565703/1021285495268982794)\n[4. ]", color=0xFF0000)

        embed2=Embed(title=f"**[- 1. Intro (NEW) -]**", 
        description=f"**Welcome to the Serpent's game!**\n\nFor starters the goal in development is to keep the game as simplistic as possible and be more a fun different Discord expierence.\nThere is currently no win conditions in the game at this time, this is planned to be changed some day.\n\n Reading throught this Handbook will be the 1 spot \"wikipedia\" for the entire game and how most things function!\nLook for the flairs in the titles such as (New or Changed) to find updates.", color=0x0000FF)

        embed3=Embed(title=f"**[- 2. The Limited Roles (NEW) -]**", 
        description=f"**Here is a list of all the current roles that are limited in amount; along with information about each and how they play!**\n\n<:foundation:1024847941665562634> **__The 05 Council__**\nThe 05 Council, known for being the Head leaders of the Foundation, is Staff for the discord server, this role can not obtain unless accepted via application.  This is the only class that has Omni-Presense being able to see every zone and area, but not being able to partipate in the game beyond using the Red Hand or things located in Site-01.\n\n<:KETER:1020576689245392937> **__SCPs__**\nThese are the driving forces of everything.  In The Serpent's Game some of these are not played by players. The lucky ones that are played by players will be the most deadly!  Sadly dying in this role, only re-contains the SCP making it available to someone else.\n\n🐍 **__Serpent's Hand__**\nSupporting force for the SCPs and an enemy to The Foundation!  Has access to the Wander's Library giving them the information advatage with access to the server logs. (Also viewable by 05, ofcourse.)  I, The Serpent could be considered the leader of this faction and give the orders.\n\n💣 **__The Chaos Insurgency__**\nAnother enemy to the Foundation, but not for the SCP's sake!  This splinter faction from the foundation now seeks out its anomalies for there purposes.  Constantly wanting to recruit anyone whos been involved with the foundation; for use as forces against the founation!\n\n<:RedRightHand:1020893683853303828> **__Red Right Hand__**\nAka. Alpha-01 is known as being the Elite guard under the 05 Council and it carries over in the Serpent's game!  The Red right hand are to do orders given by the 05 Council, being the 05 Council's main way of participating in the game.  Can only be obtain via application to the 05 Council.", color=0x00FF00)

        embed4=Embed(title=f"**[- 3. The Foundation Roles (NEW) -]**", 
        description=f"**Here is a list of all the current foundation roles; along with information about each and how they play!**\n\n🥽 **__Mobile Task Force__**\nThe special task froce sent between facilities to take control of any situations that get out of control.  Primarily ordered by Facility managers to handle specific situations; however 05 Council could use them if situations arised to the location.\n\n🔑 **__Facility Managers__**\nAs the managers of the facility you have the highest card access of Level 4.  Along with having access to Contols over many aspects of the facility.  Making the death of a Facility Manager capable of causing a lot negative consequences for the facility.\n\n🔒 **__Containment Engineers__**\nResponsible for re-securing SCPs along with doing daily tasks to keep things in the facility well managed and under control.  Has the level 3 access card and must use D-Class personel as sacrifices occasionally. A great paying job though, with little risks!\n\n👓 **__Facility Guards__**\nThe first line of defense for any facility, Responsible for protecting personel and discipline of D-Class personel.  A hard job when things go south quickly, as its usually every man for himself; ofcourse has keycard level 2 so they can move to any area within the facility.\n\n🧪 **__Scientists__**\nResponsible for doing daily tests and taks some involing D-Class personel along side SCPs.  There lives are considered the most valuable in rescue.  Key card level 1 making them stay primarily in Light Zone, requiring guards or other personel for movement.\n\n🦺 **__D-Class Personel__**\nThe prisoners, a very hard role to accomplish great things with.  As a prisoner you will not be able to do much of anything but what you are told to do.  Ofcourse if you were the 1 in a million to escape, you can only image the rewards...\n\n🎭 **__Civilian__**\nThe \"I don't want to play\" role.  Instantly turns you into a ||basic|| ||bitch.||", color=0x00FFF0)

        embed5=Embed(title=f"**[- 4.  -]**", 
        description=f"", color=0x00FFF0)

        await table.edit(content=f" ", embed=embed1)
        await msg1.edit(content=f" ", embed=embed2)
        await msg2.edit(content=f" ", embed=embed3)
        await msg3.edit(content=f" ", embed=embed4)
        await msg4.edit(content=f" ", embed=embed5)


























    @Cog.listener('on_raw_reaction_add')
    async def role_add(self, payload:RawReactionActionEvent):
        """Reaction role add handler"""

        #* Validate channel
        if payload.channel_id != self.bot.config['channels']['role_change']:
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
        if emoji == "🏹":
            await self.bot.get_cog('Verification').verify_kingussy(author=member, guild=guild)
        elif emoji == "🐾":
            scp = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['furry'])
            await member.add_roles(scp, reason="SCP Access.")
        elif emoji == "💣":
            furry = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['scp'])
            await member.add_roles(furry, reason="Furry Access.")
        elif emoji == "🚬":
            if mod.child == False:
                await self.bot.get_cog('Verification').verify_adult(author=member, guild=guild)
        elif emoji == "🍺":
            if mod.child == False:
                await self.bot.get_cog('Verification').verify_adult(author=member, guild=guild, kinda=True)
        elif emoji == "🍼":
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