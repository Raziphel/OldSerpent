
#* Discord
from discord import RawReactionActionEvent, Embed
from discord.ext.commands import Cog

import utils


# * Additions

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
        description=f"**Theta-4 \"Gardeners\" - Special Staff/Personnel**\n\nHolders of this title are typically either developers/contributors or any people that are close and deemed trustworthy by the O5 Council, with [01] \"Razi\" primarily being the one to grant this rank.\n\n**Epsilon-11 \"Nine-Tailed Fox\" - Moderator**\n\nModerators are regular staff. Their responsibilities primarily consist of moderating the SCP:SL servers and making sure it is safe and fun for the playerbase. As such, they are entrusted with most permissions to be\nable to do their duties more independently and effectively. They do not moderate the Discord server and do not have any 'dangerous' permissions on it.\n\n**Alpha-01 \"Red Right Hand\" - Administrator**\n\nAdministrators are senior staff members and are considered 'assistants' in a sense to the O5 Council. They hold authority over ranks below them and hold most permissions on the SCP:SL server. The duties of one may\nvary overtime, but they still hold the primary duty of moderating the SCP:SL servers. They are also generally a pool of candidates in the event of an O5 Council seat becoming available due to their seniority. They do not moderate the Discord server and do not have any 'dangerous' permissions on it.\n\n**O5 Council - Managing Body/Head Administrators**\n\nThe O5 Council is the managing body of the server. Anything that involves the server is under the consensus of the Council. They have all permissions on the SCP:SL servers. They are also the sole moderators for the\nDiscord server. The duties of an individual council member may vary depending on their specialization. As of writing, there are currently 9 council members.\n\n`Thank you to Kosar for making this comprehensive list`", color=0xF5AE47)

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
    async def server_info(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['server_info']) #? role change Channel

        msg1 = await ch.fetch_message(1052828325422317578) #? msg
        msg2 = await ch.fetch_message(1052828331197874176) #? msg
        msg3 = await ch.fetch_message(1052828335283122196) #? msg

        ch2 = guild.get_channel(1069729906994450462) #? Stat Channel
        msg10 = await ch2.fetch_message(1069848085167091712) #? REPORTING

        coin = self.bot.config['emotes']['coin']

        embed1=Embed(title=f"**[- SCP Server Info -]**", 
        description=f"**SCP Server connect addresses**\n**Serpent's Garden [Alpha]** `n01.infra.serpents.garden:7777`\n**Serpent's Garden [Epsilon]** `n01.infra.serpents.garden:7778`\n**Serpent's Garden [Kappa]** `n01.infra.serpents.garden:7779`\n**Serpent's Garden [Theta]** `n01.infra.serpents.garden:7782`", color=0xFF0000)

        embed2=Embed(title=f"**[- Most Common Questions -]**", 
        description=f"**Q: How can I see a comprehensive list off all the modded features on the servers?**\nA: [Click Here to veiw our google spreadsheet](https://docs.google.com/spreadsheets/d/1FuaqGm7l0sQg4JKpkvG7ooLM5Cdw-s4bu3YnpIoFKlc/edit?usp=sharing)\n\n**Q: How can I apply for staff?**\nA: [Click Here to apply for staff](https://forms.gle/u24XDb1DhPm6vdaW7)\n\n**Q: How do I claim my in-game role?**\nA:  [Click Here to sync your accounts to the servers](https://scpstats.com)\n\n**Q: How can I appeal my ban?**\nA: [Click Here to appeal your ban](https://forms.gle/HMjrzjHwDDimDQoMA)\n\n**Q: Are the plugins custom made?**\nA: Not all of them are custom made, but the best ones we have made by our dev who makes most of our plugins special & only for Serpent's Garden!", color=0x0000FF)

        embed3=Embed(title=f"**[- Coming Soon... -]**", 
        description=f"", color=0xFFFFFF)


        embed10=Embed(title=f"**[- Stats Table -]**", 
        description=f"[Most Kills](https://discord.com/channels/689534383878701223/1069729906994450462/1069745339520786472)\n[Most Deaths](https://discord.com/channels/689534383878701223/1069729906994450462/1069745366502748240)\n[Rounds Played](https://discord.com/channels/689534383878701223/1069729906994450462/1069745393723772989)\n[Most Playtime](https://discord.com/channels/689534383878701223/1069729906994450462/1069745459905708132)\n[Sodas Used](https://discord.com/channels/689534383878701223/1069729906994450462/1069745478570365010)\n[Medkits Used](https://discord.com/channels/689534383878701223/1069729906994450462/1069745499755794502)\n[Balls Used](https://discord.com/channels/689534383878701223/1069729906994450462/1069745523021586462)\n[Adrenalines Used](https://discord.com/channels/689534383878701223/1069729906994450462/1069745547096903690)\n[Most Escapes](https://discord.com/channels/689534383878701223/1069729906994450462/1069745575865614346)\n[Fastest Escape](https://discord.com/channels/689534383878701223/1069729906994450462/1069745597189460038)\n[Most Won Rounds](https://discord.com/channels/689534383878701223/1069729906994450462/1069745619402490039)\n[Most Rounds Lost](https://discord.com/channels/689534383878701223/1069729906994450462/1069745640936054784)\n[Most Pocket Escapes](https://discord.com/channels/689534383878701223/1069729906994450462/1069745667737669673)", color=0xFFFFFF)

        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg10.edit(content=f" ", embed=embed10)






    @Cog.listener('on_ready')
    async def staff_info(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['staff_info']) #? role change Channel

        msg1 = await ch.fetch_message(1064807624316567623) #? msg
        msg2 = await ch.fetch_message(1064807632877142116) #? msg
        msg3 = await ch.fetch_message(1064807639051145266) #? msg
        msg4 = await ch.fetch_message(1064807653370494986) #? msg
        msg5 = await ch.fetch_message(1064807661109002280) #? msg

        coin = self.bot.config['emotes']['coin']

        embed1=Embed(title=f"**[- Staff Info -]**", 
        description=f"**Theta-4 \"Gardeners\" - Special Staff/Personnel**\n\nHolders of this title are typically either developers/contributors or any people that are close and deemed trustworthy by the O5 Council, with [01] \"Razi\" primarily being the one to grant this rank.\n\n**Epsilon-11 \"Nine-Tailed Fox\" - Moderator**\n\nModerators are regular staff. Their responsibilities primarily consist of moderating the SCP:SL servers and making sure it is safe and fun for the playerbase. As such, they are entrusted with most permissions to be\nable to do their duties more independently and effectively. They do not moderate the Discord server and do not have any 'dangerous' permissions on it.\n\n**Alpha-01 \"Red Right Hand\" - Administrator**\n\nAdministrators are senior staff members and are considered 'assistants' in a sense to the O5 Council. They hold authority over ranks below them and hold most permissions on the SCP:SL server. The duties of one may\nvary overtime, but they still hold the primary duty of moderating the SCP:SL servers. They are also generally a pool of candidates in the event of an O5 Council seat becoming available due to their seniority. They do not moderate the Discord server and do not have any 'dangerous' permissions on it.\n\n**O5 Council - Managing Body/Head Administrators**\n\nThe O5 Council is the managing body of the server. Anything that involves the server is under the consensus of the Council. They have all permissions on the SCP:SL servers. They are also the sole moderators for the\nDiscord server. The duties of an individual council member may vary depending on their specialization. As of writing, there are currently 9 council members.\n\n`Thank you to Kosar for making this comprehensive list`", color=0xFF0000)

        embed2=Embed(title=f"**[- Discord Moderation -]**", 
        description=f"`.ban (Multiple Mentions) (Reason)`\n**Only 05 Council can run this command.**\nThis command should be simple, its used to ban multiple people at once!\nIt deletes that members last day of messages.\n\n`.mute (Multiple Mentions) (Reason)`\n**Only 05 Council can run this command.**\nThis command gives members a muted role, that is re-applied if they try to leave and rejoin!\n*Use `.unmute` to unmute them obviously.*\n\n`.adult (Mention)`\n**Only 05 Council can run this command.**\nThis command marks a member as an adult!\n\n`.child (Mention)`\n**Only 05 Council can run this command.**\nThis command marks a member as a child!", color=0x0000FF)

        embed3=Embed(title=f"**[- SCP:SL Moderation -]**", 
        description=f"This is atleast for now a rough outline of what to do!  Hopefully this system can be improved, this is the best we got for now, lmfao!\n\n**Mic Spamming / Soundboard in Spectator**\nThey should be banned for 1 month. (730 Hours)\n\n**Saying the N-Word**\nThey should be banned for 6 months. (4,380 Hours)\n\n**Pro-longing the round by Teaming or Glitched Spot**\nThey should be banned for 3 months. (2,190 Hours)\n\n**Harassment / Racism / Homophobia, Ect.**\nThey should be banned for 1 year. (8,760 Hours)\n\n`They can appeal these bans and you should mention that to them if you want.`", color=0x00FF00)

        embed4=Embed(title=f"**[- Staff Rule Book -]**", 
        description=f"**Yep, even staff have rules that they must follow!**\n\n**1.)** You take responsibility, even if you do something on \"accident\" unfortunately it is still on you!  This is obviously on a per-case basis but, staff must be held to higher a responsibility!\n\n**2.)** Never abuse your powers or so anything that would make it obvious that are staff are present! Do not show off or 'prove' points becuase you are staff.  This counts as staff abuse and will not be tolerated.\n**3.) __Golden Rule:__** Serpent's Garden are suppose to be an __Anarchy Server__ in terms of rules!  The only time staff need to step in is to call out stalling, harrassment, abuse and anything ruining the expierance for other players!!!\n\n**4.)** Staff Activity is a requirement (Excluding Gardeners) every staff is required to have __atleast 24 hours in per-month. (Which is honestly not strict in the slightest)\n\n**5.)** __Staff are expected to accept the staff code.__ All staff must be subject to the same treatment and if your actions require disipline, council will vote on what that will be done.  (This will be public to all other staff)", color=0xFFFFFF)

        embed5=Embed(title=f"**[- Coming Soon... -]**", 
        description=f"", color=0xFFFFFF)


        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f" ", embed=embed4)
        await msg5.edit(content=f" ", embed=embed5)










def setup(bot):
    x = rules_handler(bot)
    bot.add_cog(x)