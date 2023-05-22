
#* Discord
from discord import RawReactionActionEvent, Embed
from discord.ext.commands import Cog

from math import floor

import utils


# * Additions



class rules_handler(Cog):
    def __init__(self, bot):
        self.bot = bot



    @Cog.listener('on_ready')
    async def rules(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['info_channels']['rules']) #? Rules Channel

        rules1 = await ch.fetch_message(956470547426996244) #? 
        rules2 = await ch.fetch_message(956470556415361024) #? 
        rules3 = await ch.fetch_message(956470560097988649) #? 
        rules4 = await ch.fetch_message(956470570340450375) #? 

        embed1=Embed(title=f"**[- Laws of Confuct -]**", 
        description=f"**This is a list of rules on the conduct of members in this server!\nRead the punishment system!**\n\n**1.) Respect Everyone!**  Every member of Serpent's Garden deserves respect!  Keep your politics & religion at the door, this isn't the place for it!\n\n**2.) Harrassing**, Bullying and Insulting any member of Serpent's Garden isn't allowed.  You will be met with punishment, but the victim is required to notified staff of it, if it's a problem!\n\n**3.) Discord TOS,** all members of Serpent's Garden will comply with [Discord's Terms](https://discordapp.com/terms) along with [Discord's Guidelines](https://discordapp.com/guidelines).\n\n**4.) Age appropriate,** is a requirement in all channels of the Discord Server!  No NSFW or over the top explicit content is ever allowed!\n\n**5.) Exploits,** are not allowed!  Even here on the Discord, finding ways to cheat or exploit using any of the Discord Bot's on our server is never allowed and you should alert developers!\n\n**6.) Treason,** isn't allowed.  If you plan to hate and talk negatively about any staff member or Serpent's Garden it self, you will be punished.\n\n**7.) Respect the Garden for it is the Serpent's place...**", color=0xFF0000)

        embed2=Embed(title=f"**[- Staff Hierarchy -]**", 
        description=f"*These roles are in descending order.*\n\n***Executive Leading Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1104988250478743572>\n```\nObviously this role is for Owners of Serpent's Garden and in general make most of the decisions!\nNot usually an obtainable role.\n```\n<@&1109654196942282793>\n```\nThis role is for community managers.\nThey will manage the staff team / Game Server or Discord Server.\nObtainable after showing leadership as a council member.\n```\n<@&891793700932431942> \n```\nConsidered to be Head-Administrators as well as advisors for the Overseers & Overlord.\nObtainable after long term commitment as an administrator with no set time frame.\n```\n\n***Development Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1109655307682070558> \n```\nAchieved after continuously helping with development or providing services.\n```\n<@&1051307966223089755> \n```\nAchieved after providing development for servers on a regular basis.\n```\n<@&1109656536978034718> \n```\nAchieved by providing services or at least helping occasionally in the development process. \n```\n\n***Moderation Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1020893519885373450> \n```\nThe highest form of moderation staff!\nObtainable after at least a year of commitment as a Senior Moderator.\n```\n<@&1109664522479878244> \n```\nModerators that have proven they can be dependent and excelling as a moderator. \nObtained after half a year of service as a moderator.\n```\n<@&1055972422429442141> \n```\nOnce proven capable as a Junior Moderator you can be trusted as a regular moderator.\nObtained after at least a month after trial.\n```\n<@&1109665081681248266> \n```\nThis is the trial moderator role after being accepted to the staff team.\nObtained after application.\n```", color=0x47F599)

        embed3=Embed(title=f"**[- Serpent's Common Knowledge -]**", 
        description=f"**Here is some common things about the Serpent bot that every member should know!**\n\nThe Serpent is always rewarding members Coins & XP for every message, voice channel and command they run!\n\nIf you see any member with the <@&1028881308006502400> role they have lost permission to Read Message History and Sending Messages!", color=0x00FF00)

        embed4=Embed(title=f"**[- Scroll Up! -]**", 
        description=f"Please scroll up to read the server rules!", color=0x0000FF)


        await rules1.edit(content=f" ", embed=embed1)
        await rules2.edit(content=f" ", embed=embed2)
        await rules3.edit(content=f" ", embed=embed3)
        await rules4.edit(content=f" ", embed=embed4)










    @Cog.listener('on_ready')
    async def server_info(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['server_info']) #? role change Channel

        msg1 = await ch.fetch_message(1052828325422317578) #? msg
        msg2 = await ch.fetch_message(1052828331197874176) #? msg
        msg3 = await ch.fetch_message(1052828335283122196) #? msg

        coin = self.bot.config['emotes']['coin']

        embed1=Embed(title=f"**[- SCP Server Info -]**", 
        description=f"**SCP Server connect addresses**\n**Serpent's Garden [Alpha]** `n01.infra.serpents.garden:7777`\n**Serpent's Garden [Epsilon]** `n01.infra.serpents.garden:7778`\n**Serpent's Garden [Kappa]** `n01.infra.serpents.garden:7779`\n**Serpent's Garden [Theta]** `n01.infra.serpents.garden:7782`", color=0xFF0000)

        embed2=Embed(title=f"**[- Most Common Questions -]**", 
        description=f"**Q: How can I see a comprehensive list off all the modded features on the servers?**\nA: <#1096531445792657439>\n\n**Q: How can I apply for staff?**\nA: <#1080592426965684255>\n\n**Q: How do I claim my in-game roles?**\nA:  [Click Here to sync your accounts to the servers](https://discord.com/api/oauth2/authorize?response_type=code&client_id=749684016550248490&scope=connections%20identify&redirect_uri=https://accounts.cedmod.nl/Auth/DiscordSSO&state=476547)\n\n**Q: How can I appeal my ban?**\nA: <#1080592426965684255>\n\n**Q: Are the plugins custom made?**\nA: Not all of them are custom made, but the best ones we have made by our dev who makes most of our plugins special & only for Serpent's Garden!\n\n**Q: Where can I see the server's player leaderboard**\nA: <#1052823837416357999>\n\n**Q: Where can I see a full report everytthing in a round?**\nA: <#1065409585764106321>", color=0x0000FF)

        embed3=Embed(title=f"**[- Coming Soon... -]**", 
        description=f"", color=0xFFFFFF)


        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)






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
        description=f"**Gardeners**\n\nHolders of this title are typically either developers/contributors or any people that are close and deemed trustworthy by the Council, with [01] \"Razi\" primarily being the one to grant this rank.  They contribute to the server in some sort of way!\n\n**Moderator**\n\nModerators are regular staff. Their responsibilities primarily consist of moderating the SCP:SL servers and making sure it is safe and fun for the playerbase. As such, they are entrusted with most permissions to be\nable to do their duties more independently and effectively. They do not moderate the Discord server and do not have any 'dangerous' permissions on it.\n\n**Administrator**\n\nAdministrators are senior staff members and are considered 'assistants' in a sense to the Council. They hold authority over ranks below them and hold most permissions on the SCP:SL server. The duties of one may\nvary overtime, but they still hold the primary duty of moderating the SCP:SL servers. They are also generally a pool of candidates in the event of an Council seat becoming available due to their seniority. They do not moderate the Discord server and do not have any 'dangerous' permissions on it.\n\n**Council**\n\nThe Council is the managing body of the server. Anything that involves the server is under the consensus of the Council. They have all permissions on the SCP:SL servers. They are also the sole moderators for the\nDiscord server. The duties of an individual council member may vary depending on their specialization. As of writing, there are currently 9 council members.\n\n`Thank you to Kosar for making this comprehensive list`", color=0xFF0000)

        embed2=Embed(title=f"**[- Discord Moderation -]**", 
        description=f"`.ban (Multiple Mentions) (Reason)`\n**Only 05 Council can run this command.**\nThis command should be simple, its used to ban multiple people at once!\nIt deletes that members last day of messages.\n\n`.mute (Multiple Mentions) (Reason)`\n**Only 05 Council can run this command.**\nThis command gives members a muted role, that is re-applied if they try to leave and rejoin!\n*Use `.unmute` to unmute them obviously.*\n\n`.adult (Mention)`\n**Only 05 Council can run this command.**\nThis command marks a member as an adult!\n\n`.child (Mention)`\n**Only 05 Council can run this command.**\nThis command marks a member as a child!", color=0x0000FF)

        embed3=Embed(title=f"**[- SCP:SL Moderation -]**", 
        description=f"This is atleast for now a rough outline of what to do!  Hopefully this system can be improved, this is the best we got for now, lmfao!\n\n**Mic Spamming / Soundboard in Spectator**\nThey should be banned for 1 month. (730 Hours)\n\n**Saying the N-Word**\nThey should be banned for 6 months. (4,380 Hours)\n\n**Pro-longing the round by Teaming or Glitched Spot**\nThey should be banned for 3 months. (2,190 Hours)\n\n**Harassment / Racism / Homophobia, Ect.**\nThey should be banned for 1 year. (8,760 Hours)\n\n`They can appeal these bans and you should mention that to them if you want.`", color=0x00FF00)

        embed4=Embed(title=f"**[- SCP Staff Rule Book -]**", 
        description=f"**Yep, even staff have rules that they must follow!**\n\n**1.)** You take responsibility, even if you do something on \"accident\" unfortunately it is still on you!  This is obviously on a per-case basis but, staff must be held to higher a responsibility!\n\n**2.)** Never abuse your powers or so anything that would make it obvious that are staff are present! Do not show off or 'prove' points becuase you are staff.  This counts as staff abuse and will not be tolerated.\n\n**3.) __Golden Rule:__** Serpent's Garden are suppose to be an __Anarchy Server__ in terms of rules!  The only time staff need to step in is to call out stalling, harrassment, abuse and anything ruining the experience for other players!!!\n\n**4.)** Staff Activity is a requirement (Excluding Gardeners) every staff is required to have __atleast 24 hours per-month on the SCP servers!__ (Which is honestly not strict in the slightest)\n\n**5.)** __Staff are expected to accept the staff code.__ All staff must be subject to the same treatment and if your actions require disipline, council will vote on what that will be done.  (This will be public to all other staff)", color=0xFF00FF)

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