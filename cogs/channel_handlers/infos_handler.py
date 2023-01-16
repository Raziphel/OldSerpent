
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
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['rules']) #? Rules Channel

        rules1 = await ch.fetch_message(956470547426996244) #? 
        rules2 = await ch.fetch_message(956470556415361024) #? 
        rules3 = await ch.fetch_message(956470560097988649) #? 
        rules4 = await ch.fetch_message(956470570340450375) #? 
        rules5 = await ch.fetch_message(956470575411388436) #? 

        embed1=Embed(title=f"**[- The Server's Rules -]**", 
        description=f"**These are rules for the entire Discord Server.**\n\n**1.)** Respect Everyone, not a single person doesn't deserve respect, especially the 05 Council.\n\n**2.)** Harrassment, Bully, Attacking of any kind or form of any member on this server isnt allowed. Period.\n\n**3.)** Drama, most people here have already gone through highschool, don't bring it back.\n\n**4.)** This server only allows the use of English.  We can not moderate other languages.\n\n**5.)** Common Sense, Don't be annoying or do anything that would make a 05 Council have to punish. (Should be easy.)\n\n**6.)** Discord TOS, obviously don't do anything discord already doesn't allow, could count as previous rule.\n\n**7.)** Respect The Serpent.", color=0xF54747)

        embed2=Embed(title=f"**[- SCP Server Rules -]**", 
        description=f"**If you are looking for information related SCP servers check #server-info for most things you'd meed!**\n\n**1.** No hate speech, harassment or bigotry.  Anything racist, homophobic, Ect. is not allowed.  \n\n**2.** No mic-spam is allowed at all and soundboards are not allowed in spectator chat or radio.\n\n**3.** This server is intended for mature audiences!  Staff can and will mute for underage voices. \n\n**4.** Staff members reserve the right to punish players just for disrespect.  They deserve at least that. \n\n**5.** Teaming is generally allowed, so long as it doesn’t stall the round.\n\n**6.** Do not grief other players on your team!  Intentionally killing your allies is never allowed.\n\n**7.** Do not abuse any exploits to lag the server or gain some other unfair advantage over others. Glitching into bugged spots on the map is allowed as long as it doesn't pro-long the round! \n\n**8.** No advertisements of any form, including over the intercom or in voice chat.", color=0x47F599)

        embed3=Embed(title=f"**[- The Staff System -]**", 
        description=f"**Zeta-9 \"Mole Rats\" - Trial Moderator**\n\nConsisting of recently accepted staff, trial moderators undergoo a trial process to become fully fledged staff. During their trial period, they will be guided and overseen carefully to make sure they are approrpiate\nfor a fully fledged position. They will have necessary permissions to perform their duties in the SCP:SL servers, and any situations out of their boundaries would require them to ask for assistance.\n\n**Theta-4 \"Gardeners\" - Special Staff/Personnel**\n\nHolders of this title are typically either developers/contributors or any people that are close and deemed trustworthy by the O5 Council, with [01] \"Razi\" primarily being the one to grant this rank.\n\n**Epsilon-11 \"Nine-Tailed Fox\" - Moderator**\n\nModerators are regular staff. Their responsibilities primarily consist of moderating the SCP:SL servers and making sure it is safe and fun for the playerbase. As such, they are entrusted with most permissions to be\nable to do their duties more independently and effectively. They do not moderate the Discord server and do not have any 'dangerous' permissions on it.\n\n**Alpha-01 \"Red Right Hand\" - Administrator**\n\nAdministrators are senior staff members and are considered 'assistants' in a sense to the O5 Council. They hold authority over ranks below them and hold most permissions on the SCP:SL server. The duties of one may\nvary overtime, but they still hold the primary duty of moderating the SCP:SL servers. They are also generally a pool of candidates in the event of an O5 Council seat becoming available due to their seniority. They do not moderate the Discord server and do not have any 'dangerous' permissions on it.\n\n**O5 Council - Managing Body/Head Administrators**\n\nThe O5 Council is the managing body of the server. Anything that involves the server is under the consensus of the Council. They have all permissions on the SCP:SL servers. They are also the sole moderators for the\nDiscord server. The duties of an individual council member may vary depending on their specialization. As of writing, there are currently 9 council members.\n\nThank you to Kosar for making this comprehensive list.", color=0xF5AE47)

        embed4=Embed(title=f"**[- Moderation System -]**", 
        description=f"**By absolutely no means do the 05 Council (Staff) have to be \"Fair\", in any situation or decision. They are put there for a reason and we usually run everything past one another.**\n\nFor most situations a Council member will give a single warning and after that you are completely fair game; from that council member or any other for whatever punishment they believe you deserve.  Lying about your age, breaking Discord TOS, sending spam, hate, phishing links or scamming in anyway, is awlays going to be a ban with no warning.  *It won't be tolerated at all.*\n\n**This server requires a phone number attached to the Discord Account!**\nWe do this to keep every member on the discord hopefully safe from scams and being able to weave out bad apples.", color=0xB6F547)

        embed5=Embed(title=f"**[- The Serpent & Leaving -]**", 
        description=f"*The Serpent is the Discord bot used to play the Serpent's game*\n\nIt uses the prefix `.` and doesn't like slash commands!  It is quite important you have your settings set up where you can recieve private message from the Serpent! \n\n**What happens when you leave the Serpent's Garden Discord Server?**\n*if you leave the Serpent's Garden, your levels and coins are lost.  This includes getting banned or kicked.*", color=0x89F547)


        await rules1.edit(content=f" ", embed=embed1)
        await rules2.edit(content=f" ", embed=embed2)
        await rules3.edit(content=f" ", embed=embed3)
        await rules4.edit(content=f" ", embed=embed4)
        await rules5.edit(content=f" ", embed=embed5)





    @Cog.listener('on_ready')
    async def role_change(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['role_change']) #? role change Channel

        msg1 = await ch.fetch_message(1029973755428093986) #? msg
        msg2 = await ch.fetch_message(1029973761673408543) #? msg
        msg3 = await ch.fetch_message(1029973773656531015) #? msg
        msg4 = await ch.fetch_message(1029975810251169873) #? msg
        
        coin = self.bot.config['emotes']['coin']

        embed1=Embed(title=f"**[- Level Roles -]**", 
        description=f"This is the levels you recieve each role at! Any other roles are probably staff or a donator role!\n\n**Level 100 ->** `Serpent's Hand`\n**Level 90 ->** `Gamers Against Weed`\n**Level 80 ->** `Chaos Insurgency`\n**Level 75 ->** `Children of the Scarlet King`\n**Level 70 ->** `Sarkic Cult`\n**Level 65 ->** `Church of the Broken God`\n**Level 60 ->** `Global Occult Coalition`\n**Level 55 ->** `Unusual Incidents Unit`\n**Level 50 ->** `Ethics Committee`\n**Level 45 ->** `Memetics Division`\n**Level 40 ->** `Site Director`\n**Level 35 ->** `Facility Manager`\n**Level 30 ->** `MTF Operative`\n**Level 25 ->** `Sequrity Officer`\n**Level 20 ->** `Containment Specialist`\n**Level 15 ->** `Head-Reseracher`\n**Level 10 ->** `Scientist`\n**Level 5 ->** `D-Class`\n**Level 0 ->** `Janitor`", color=0xFF0000)

        embed2=Embed(title=f"**[- Pickable Roles -]**", 
        description=f"☢ `SCP Ping`\nAnyone can ping you with this role!\nIts only to be used when notifying people to play SCP!\n\n🍙`Weebs`\nGives you access to the Anime channel... Oh no.\n\n🌈`LGBT`\nSingals that you support or are LGBT! c:\n\n🐾 `Furry`\nThis role is for those degenerates!", color=0x0000FF)

        embed3=Embed(title=f"**[- Update Pings -]**", 
        description=f"**These roles are pinged by staff only.  Anyone who pings the role will be banned.** *So atleast if ya do get pinged and its not staff! Ya get to see someone banned! :)*\n\n🔔 `Discord Pings`\nThese are pings focused towards the Discord Server!.\n\n🧪 `Server Pings`\nThese are pings focused towards the SCP Servers!. ", color=0xFFFFFF)

        embed4=Embed(title=f"**[- Age Roles -]**", 
        description=f"**These roles are permenant will require DMing or pinging 05 Council to change.**\n\n🚬 `Adult`\nThis will give you access to any Adult marked channels in any category on the server.  There is still no NSFW allowed on this server at all.\n\n🍼 `Child`\nThis lets people know your a child.\nIt is encouraged to get this role and not lie..", color=0xFF00FF)

        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f" ", embed=embed4)









    @Cog.listener('on_ready')
    async def server_info(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['server_info']) #? role change Channel

        msg1 = await ch.fetch_message(1052828325422317578) #? msg
        msg2 = await ch.fetch_message(1052828331197874176) #? msg
        msg3 = await ch.fetch_message(1052828335283122196) #? msg

        ch2 = guild.get_channel(1052824545146445885) #? role change Channel
        msg10 = await ch2.fetch_message(1052854912381374514) #? REPORTING

        coin = self.bot.config['emotes']['coin']

        embed1=Embed(title=f"**[- SCP Server Info -]**", 
        description=f"**SCP Server connect addresses**\nSerpent's Garden [Alpha] `n01.infra.serpents.garden:7777`\nSerpent's Garden [Epsilon] `n01.infra.serpents.garden:7778`\nSerpent's Garden [Kappa] `n01.infra.serpents.garden:7779`\nSerpent's Garden [Theta] `n01.infra.serpents.garden:7782`", color=0xFF0000)

        embed2=Embed(title=f"**[- Most Common Questions -]**", 
        description=f"**Q: How can I see a comprehensive list off all the modded features on the servers?**\nA: [Click Here to veiw our google spreadsheet](https://docs.google.com/spreadsheets/d/1FuaqGm7l0sQg4JKpkvG7ooLM5Cdw-s4bu3YnpIoFKlc/edit?usp=sharing)\n\n**Q: How can I apply for staff?**\nA: We currently do not have applications open yet.\n\n**Q: How do I claim my in-game role?**\nA:  [Click Here to sync your accounts to the servers](https://serpents_garden.cmod.app)\n\n**Q: How can I appeal my ban?**\nA: [Click Here to appeal your ban](https://serpents_garden.cmod.app)", color=0x0000FF)

        embed3=Embed(title=f"**[- Coning Soon... -]**", 
        description=f"", color=0xFFFFFF)


        embed10=Embed(title=f"**[- Creating a report! -]**", 
        description=f"**You can create reports on players in the SCP server, using this simple reporting tool!**\n\nEven if staff are not in the server they can punish from these reports and moderate easily!  Please use these over the in-game reports since you already using the Discord!  (Which we thank you for!)\n\nIf your report is not on the list of pre-defined reports its may not be against our rules!", color=0xFFFFFF)

        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg10.edit(content=f" ", embed=embed10)




















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
            await utils.UserFunction.verify_user(user=member, type='alliance')
        elif emoji == "🐾": 
            await utils.UserFunction.verify_user(user=member, type='furry')
        elif emoji == "🚬":
            if mod.child == False:
                await self.bot.get_cog('Verification').verify_adult(author=member, guild=guild)
        elif emoji == "🍼":
            mod.child = True
            child = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['child'])
            await member.add_roles(child, reason="Marked as child.")
        elif emoji == "🧪":
            updates = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['server_updates'])
            await member.add_roles(updates, reason="Will get updates now.")
        elif emoji == "🔔":
            updates = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['discord_updates'])
            await member.add_roles(updates, reason="Will get updates now.")
        elif emoji == "☢":
            updates = utils.DiscordGet(guild.roles, id=1062945474757271564)
            await member.add_roles(updates, reason="Will get updates now.")
        elif emoji == "🍙":
            updates = utils.DiscordGet(guild.roles, id=1057833430685057146)
            await member.add_roles(updates, reason="Will get updates now.")
        elif emoji == "🌈":
            updates = utils.DiscordGet(guild.roles, id=1057833439518261292)
            await member.add_roles(updates, reason="Will get updates now.")

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