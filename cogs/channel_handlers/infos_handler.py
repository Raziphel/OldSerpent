
#* Discord
from discord import RawReactionActionEvent, Embed
from discord.ext.commands import Cog

from math import floor

import utils


# * Additions



class rules_handler(Cog):
    def __init__(self, bot):
        self.bot = bot



    @Cog.listener('on_ready') #! ---> Server Rules
    async def rules(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['info_channels']['rules']) #? Rules Channel

        rules1 = await ch.fetch_message(1134121709142806659) #? 
        rules2 = await ch.fetch_message(1134121730366001262) #? 
        rules3 = await ch.fetch_message(1134121747252248637) #? 
        rules4 = await ch.fetch_message(1134121762561470626) #? 
        rules5 = await ch.fetch_message(1134121781196763256) #? 
        rules6 = await ch.fetch_message(1134121813954277416) #? 
        rules7 = await ch.fetch_message(1134121834737049621) #? 
        rules8 = await ch.fetch_message(1134121863577079898) #? 

        embed1=Embed(description=f"```fix\n█ 1. Server Etiquette █\n```\n⦁ Try to maintain the natural flow of a conversation already in progress. Do not spam, post irrelevant images or purposely disrupt the chat in any way.\n⦁ Avoid sending repeating messages as well as repeated characters, emojis or phrases.\n⦁ Try to keep your messages together. Avoid breaking your paragraphs up into multiple lines and sending messages too quickly.\n⦁ Keep roleplay short and casual. The occasional head-pat, hug or high-five is fine, but limit non-conversation to only one or two messages.\n⦁ This is an English-speaking server. Please communicate in a way our members and staff can understand while participating in this server.", color=0x80F75C)

        embed2=Embed(description=f"```fix\n█ 2. Respect █\n```\nExcessively argumentative, rude, dismissive, or aggressive members will be removed. We will not tolerate any instances of offensive behaviour towards anyone, nor any occurrences of racism, homophobia, transphobia or other types of discriminatory language. Jokes about these topics are equally unwelcome. Personal arguments or conversations between members should be taken to direct messages if both users wish to continue, rather than affecting the atmosphere/mood/feeling of the chat.", color=0x80F75C)


        embed3=Embed(description=f"```fix\n█ 3. Mental Illness █\n```\nThis includes jokes and discussing methods of harm. We care about the well-being of all our members; however, this chat is not a suitable method of mental care therapy. Instead, if you or somebody you know needs help, please seek out trained professionals for appropriate care. Resources relating to these issues can be found here (Click Here)[https://www.ispn-psych.org/mental-health-links]\nThis rule isn't included in an attempt to deny people an emotional outlet, but instead to protect those members from malicious users who might try to convince them to harm themselves and to protect them from armchair psychologists who may make things worse.", color=0x80F75C)

        embed4=Embed(description=f"```fix\n█ 4. Staff Decisions █\n```\nIf any issue comes up, please ping the appropriate staff for assistance. Please do not attempt to resolve issues yourself. Staff' decisions and actions should be respected by all users; however users may contact the team for additional information, clarification or to appeal. If you have any issues with a particular staff's actions please take it to an <@&1104988250478743572> or <@&1109654196942282793> privately.\n\nIn the case of emergencies or issues that require immediate attention you can:\nPing us using <@&1068389119195107378> Please do not use this for non-emergencies.", color=0x80F75C)

        embed5=Embed(description=f"```fix\n█ 5. Advertising █\n```\nAdvertisements to other groups or Discord servers are not allowed without prior staff approval. Members seeking to advertise commissions or other products must do so in the art sectioned channels. Advertisements should not include any NSFW or otherwise unsuitable content. We consider raffles, or anything which requires following, liking, retweeting, and so forth, as advertising.", color=0x80F75C)

        embed6=Embed(description=f"```fix\n█ 6. Politics █\n```\nPolitical topics may be discussed, but must be held within the discussions channels (<#1134120143132307616>⁠). Please try to avoid any heated political discussions. This includes, but is not limited to, inflammatory remarks, stances or controversial topics, takes or media. Political imagery or references are also not suitable for inclusion in profile pictures, nicknames or emojis. This ranges from Communist and Fascist symbolism, to modern day mainstream politics and political movements. Keep rule #2 in mind and treat each other with respect during discourse.", color=0x80F75C)

        embed7=Embed(description=f"```fix\n█ 7. NSFW Content █\n```\nDo not post any sexually explicit, suggestive or excessively violent content.\n⦁ This applies to all forms of content. Text, images, profile pictures, statuses, etc.\n⦁ Featureless anatomy (i.e.: cartoon / barbie doll nudity) is okay.\n⦁ Images that are sexually themed or where any part of a character is featured in a sexually suggestive manner are not allowed.\n⦁ Excessive or detailed gore is not permitted.\n⦁ No questionable underage content of any kind.\n⦁ No content that could be considered to be depicting a fetish, regardless of whether some may consider it SFW.\n⦁ No alluding to or mentioning content disallowed by these rules. This includes but is not limited to phrases, imagery or external sites.\n⦁ If you are unsure whether or not something is considered SFW according to this server's rules, message a mod for clarification.", color=0x80F75C)

        embed8=Embed(description=f"```fix\n█ 8. Alt Accounts █\n```\nDue to potential user abuse, users are not allowed to have alts within the server. If a user is found with an alt, the alt(s) and main account will be removed. Please keep any and all alts out of the server.", color=0x80F75C)

        await rules1.edit(content=f" ", embed=embed1)
        await rules2.edit(content=f" ", embed=embed2)
        await rules3.edit(content=f" ", embed=embed3)
        await rules4.edit(content=f" ", embed=embed4)
        await rules5.edit(content=f" ", embed=embed5)
        await rules6.edit(content=f" ", embed=embed6)
        await rules7.edit(content=f" ", embed=embed7)
        await rules8.edit(content=f" ", embed=embed8)





    @Cog.listener('on_ready') #! ---> No Channels
    async def no_channels_info(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['info_channels']['no_channels']) #? No channels Channel

        msg1 = await ch.fetch_message(1133002927678697572) #? msg
        msg2 = await ch.fetch_message(1133009889204121701) #? msg
        msg3 = await ch.fetch_message(1133086049590059078) #? msg
        msg4 = await ch.fetch_message(1134113997378027582) #? msg

        embed1=Embed(description=f"```fix\n█ Not able to see any channels? █\n```\nAre you not able to see any channels?  Or maybe you're missing some channels!?\n\n**You can get access to multiple different areas in the server using <id:customize>!**\n\nSerpent's Garden is a large community with many different areas, that not everyone wants to be able to see!  That's why it is setup this way.", color=0xFFFFFF)

        embed2=Embed(description=f"```fix\n█ Channel Quick Fix! █\n```\nIf you are looking for a quick fix becuase you've just recently lost access to some channels, or some have just disapeared.\n\n**Consider clicking `Show All Channels` as seen below!**", color=0xFFFFFF)
        embed2.set_image(url="https://cdn.discordapp.com/attachments/550556052396179458/1133009744609673308/image.png")

        embed3=Embed(description=f"```fix\n█ Staff Hierarchy █\n```\n*These roles are in descending order.*\n\n***Executive Leading Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1104988250478743572>\n```\nObviously this role is for Owners of Serpent's Garden and in general make most of the decisions!\nNot usually an obtainable role.\n```\n<@&1109654196942282793>\n```\nThis role is for community managers.\nThey will manage the staff team / Game Server or Discord Server.\nObtainable after showing leadership as a council member.\n```\n<@&891793700932431942> \n```\nConsidered to be Head-Administrators as well as advisors for the Overseers & Overlord.\nObtainable after long term commitment as an administrator with no set time frame.\n```\n\n***Development Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1109655307682070558> \n```\nAchieved after continuously helping with development or providing services.\n```\n<@&1051307966223089755> \n```\nAchieved after providing development for servers on a regular basis.\n```\n<@&1109656536978034718> \n```\nAchieved by providing services or at least helping occasionally in the development process. \n```\n\n***Moderation Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1020893519885373450> \n```\nThe highest form of moderation staff!\nObtainable after at least a year of commitment as a Senior Moderator.\n```\n<@&1109664522479878244> \n```\nModerators that have proven they can be dependent and excelling as a moderator. \nObtained after half a year of service as a moderator.\n```\n<@&1055972422429442141> \n```\nOnce proven capable as a Junior Moderator you can be trusted as a regular moderator.\nObtained after at least a month after trial.\n```\n<@&1109665081681248266> \n```\nThis is the trial moderator role after being accepted to the staff team.\nObtained after application.\n```", color=0x47F599)

        embed4=Embed(description=f"```fix\n█ The Access Roles! █\n```\n<@&1054143874538426368> gives access to most of the general open channels!\Channels: art, media, memes.\n\n<@&1107421191586726039> gives access to channels related to the SCP:SL Servers.\nChannels: SL-Info, SL-Plugins, Round Reports\n\n<@&1129464175396143104> gives access to furry related channels!\nExamples: Fur-Den, Furry-Art, Sona-posts.\n\n<@&1116039697785950318> a private role for friends of Razi.\nChannels: Occult Hall, Occult VC, Edgy Memes.\n\n<@&1113180697511874653> a private role for members of the Poop...\nChannels: Poop Shenanigans", color=0xFFFFFF)


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

        coin = self.bot.config['emotes']['coin']

        embed1=Embed(description=f"```fix\n█ SCP Server Info █\n```\n**SCP Server connect addresses**\n**Serpent's Garden [Alpha]** `n01.infra.serpents.garden:7777`\n**Serpent's Garden [Epsilon]** `n01.infra.serpents.garden:7778`\n**Serpent's Garden [Kappa]** `n01.infra.serpents.garden:7779`\n**Serpent's Garden [Theta]** `n01.infra.serpents.garden:7782`", color=0xFF0000)

        embed2=Embed(description=f"```fix\n█ Most Common Questions █\n```\n**Q: How can I see a comprehensive list off all the modded features on the servers?**\nA: <#1096531445792657439>\n\n**Q: How can I apply for staff?**\nA: <#1080592426965684255>\n\n**Q: How do I claim my in-game roles?**\nA:  [Click Here to sync your accounts to the servers](https://discord.com/api/oauth2/authorize?response_type=code&client_id=749684016550248490&scope=connections%20identify&redirect_uri=https://accounts.cedmod.nl/Auth/DiscordSSO&state=476547)\n\n**Q: How can I appeal my ban?**\nA: <#1080592426965684255>\n\n**Q: Are the plugins custom made?**\nA: Not all of them are custom made, but the best ones we have made by our dev who makes most of our plugins special & only for Serpent's Garden!\n\n**Q: Where can I see the server's player leaderboard**\nA: <#1052823837416357999>\n\n**Q: Where can I see a full report everytthing in a round?**\nA: <#1065409585764106321>", color=0x0000FF)

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
        description=f"`/ban (Multiple Mentions) (Reason)`\n**Only Upper Management can run this command.**\nThis command should be simple, its used to ban multiple people at once!\nIt deletes that members last day of messages.\n\n`/mute (Multiple Mentions) (Reason)`\nThis command gives members a muted role, that is re-applied if they try to leave and rejoin!\n*Use `/unmute` to unmute them obviously.*\n\n`/imageban (Mention)`\n**Only Upper Management can run this command.**\nThis command takes away image permissions in general from a user.", color=0x0000FF)

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