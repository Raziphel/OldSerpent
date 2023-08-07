
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


        embed3=Embed(description=f"```fix\n█ 3. Mental Illness █\n```\nThis includes jokes and discussing methods of harm. We care about the well-being of all our members; however, this chat is not a suitable method of mental care therapy. Instead, if you or somebody you know needs help, please seek out trained professionals for appropriate care. Resources relating to these issues can be found [Here](https://www.ispn-psych.org/mental-health-links).\n\n This rule isn't included in an attempt to deny people an emotional outlet, but instead to protect those members from malicious users who might try to convince them to harm themselves and to protect them from armchair psychologists who may make things worse.", color=0x80F75C)

        embed4=Embed(description=f"```fix\n█ 4. Staff Decisions █\n```\nIf any issue comes up, please ping the appropriate staff for assistance. Please do not attempt to resolve issues yourself. Staff' decisions and actions should be respected by all users; however users may contact the team for additional information, clarification or to appeal. If you have any issues with a particular staff's actions please take it to an <@&1104988250478743572> or <@&1109654196942282793> privately.\n\nIn the case of emergencies or issues that require immediate attention you can:\nPing us using <@&1068389119195107378> Please do not use this for non-emergencies.", color=0x80F75C)

        embed5=Embed(description=f"```fix\n█ 5. Advertising █\n```\nAdvertisements to other groups or Discord servers are not allowed without prior staff approval. Members seeking to advertise commissions or other products must do so in the art sectioned channels. Advertisements should not include any NSFW or otherwise unsuitable content. We consider raffles, or anything which requires following, liking, retweeting, and so forth, as advertising.\n\nChoosing to DM any member of the server only to try and advertise will result in an instant ban, especially if you are a low level member.", color=0x80F75C)

        embed6=Embed(description=f"```fix\n█ 6. Politics █\n```\nPolitical topics may be discussed, but must be held within the discussions channels (<#1134120143132307616>⁠). Please try to avoid any heated political discussions. This includes, but is not limited to, inflammatory remarks, stances or controversial topics, takes or media. Political imagery or references are also not suitable for inclusion in profile pictures, nicknames or emojis. This ranges from Communist and Fascist symbolism, to modern day mainstream politics and political movements. Keep rule #2 in mind and treat each other with respect during discourse.", color=0x80F75C)

        embed7=Embed(description=f"```fix\n█ 7. NSFW Content █\n```\nDo not post any sexually explicit, suggestive or excessively violent content.\n\n⦁ This applies to all forms of content. Text, images, profile pictures, statuses, etc.\n⦁ Featureless anatomy (i.e.: cartoon / barbie doll nudity) is okay.\n⦁ Images that are sexually themed or where any part of a character is featured in a sexually suggestive manner are not allowed.\n⦁ Excessive or detailed gore is not permitted.\n⦁ No questionable underage content of any kind.\n⦁ No content that could be considered to be depicting a fetish, regardless of whether some may consider it SFW.\n⦁ No alluding to or mentioning content disallowed by these rules. This includes but is not limited to phrases, imagery or external sites.\n⦁ If you are unsure whether or not something is considered SFW according to this server's rules, message a mod for clarification.", color=0x80F75C)

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
        msg5 = await ch.fetch_message(1134171819444805662) #? msg
        msg6 = await ch.fetch_message(1134568608979234846) #? msg
        
        
        
        lastmsg = await ch.fetch_message(1134568710112301086) #? msg

        coin = self.bot.config['emotes']['coin']

        embed1=Embed(description=f"```fix\n█ Staff Hierarchy █\n```\n*These roles are in descending order.*\n\n***Executive Leading Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1104988250478743572>\n```\nObviously this role is for Owners of Serpent's Garden and in general make most of the decisions!\nNot usually an obtainable role.\n```\n<@&1109654196942282793>\n```\nThis role is for community managers.\nThey will manage the staff team / Game Server or Discord Server.\nObtainable after showing leadership as a council member.\n```\n<@&891793700932431942> \n```\nConsidered to be Head-Administrators as well as advisors for the Overseers & Overlord.\nObtainable after long term commitment as an administrator with no set time frame.\n```\n\n***Development Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1109655307682070558> \n```\nAchieved after continuously helping with development or providing services.\n```\n<@&1051307966223089755> \n```\nAchieved after providing development for servers on a regular basis.\n```\n<@&1109656536978034718> \n```\nAchieved by providing services or at least helping occasionally in the development process. \n```\n\n***Moderation Staff Roles***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<@&1020893519885373450> \n```\nThe highest form of moderation staff!\nObtainable after at least a year of commitment as a Senior Moderator.\n```\n<@&1109664522479878244> \n```\nModerators that have proven they can be dependent and excelling as a moderator. \nObtained after half a year of service as a moderator.\n```\n<@&1055972422429442141> \n```\nOnce proven capable as a Junior Moderator you can be trusted as a regular moderator.\nObtained after at least a month after trial.\n```\n<@&1109665081681248266> \n```\nThis is the trial moderator role after being accepted to the staff team.\nObtained after application.\n```", color=0x47F599)

        embed2=Embed(description=f"```fix\n█ Not able to see any channels? █\n```\nAre you not able to see any channels?  Or maybe you're missing some channels!?\n\n**You can get access to multiple different areas in the server using <id:customize>!**\n\nSerpent's Garden is a large community with many different areas, that not everyone wants to be able to see!  That's why it is setup this way.", color=0x47F599)

        embed3=Embed(description=f"```fix\n█ Channel Quick Fix! █\n```\nIf you are looking for a quick fix becuase you've just recently lost access to some channels, or some have just disapeared.\n\n**Consider clicking `Show All Channels` as seen below!**", color=0x47F599)
        embed3.set_image(url="https://cdn.discordapp.com/attachments/550556052396179458/1133009744609673308/image.png")

        embed4=Embed(description=f"```fix\n█ The Access Roles! █\n```\n<@&1054143874538426368> gives access to most of the general open channels!\nChannels: art, media, memes.\n\n<@&1107421191586726039> gives access to channels related to the SCP:SL Servers.\nChannels: SL-Info, SL-Plugins, Round Reports\n\n<@&1129464175396143104> gives access to furry related channels!\nExamples: Fur-Den, Furry-Art, Sona-posts.\n\n<@&1116039697785950318> a private role for friends of Razi.\nChannels: Occult Hall, Occult VC, Edgy Memes.\n\n<@&1113180697511874653> a private role for members of the Poop...\nChannels: Poop Shenanigans", color=0x47F599)

        embed5=Embed(description=f"```fix\n█ Serpent's Economy █\n```\nEvery new member joining the server is given **1,000x {coin} to start out with!**  You can gain these coins by sending messages in chat every couple of seconds.  Being in a vc for longer than 10 minutes, clicking on random rewards that appear and many other ways!  Usually when you gain coins you also are gaining XP as well!  The coins on the server have a finite amount to be more similar to an actual economy!\n\nThe Serpent bot itself gives its coins, when you or anyone else gains coins, along with that all the taxing and purchasing in the <#946730953731100682> goes to the Serpent!  Occasionaly coins are added in to the economy, to keep the Serpent bot from ever reaching 0 coins.\n\n**Taxation:** The bot usually will tax (ex: lottery winner) with an 8% tax!  This also applies to sending coins to another user on the server.  In addition to taxes on the movement & winnings of coins the bot taxes at a rate of **25x {coin} per hour**! This is just another measure to make sure inactive members with lots of coins, get there coins back in to the economy.", color=0x47F599)

        embed6=Embed(description=f"```fix\n█ Leaving Punishments █\n```\nAny member who decides to leave, is kicked or even banned.  Have all there coins given back to the Serpent!  So keep in mind if you ever decide to leave that you will not only lose all your coins!  But, any purchases you had made with those coins as well.\n\nThis is to keep the economy functioning properly and as another defensive measure against bad actors who get banned.", color=0x47F599)

        lastembed=Embed(description=f"```fix\n█ Help Guide █\n```\n\n1.) [Staff Hierarchy](https://discord.com/channels/689534383878701223/1133002668189700116/1133002927678697572)\n2.) [Not able to see any Channels?](https://discord.com/channels/689534383878701223/1133002668189700116/1133009889204121701)\n3.) [Channel Quick Fix](https://discord.com/channels/689534383878701223/1133002668189700116/1133086049590059078)\n4.) [The Access Roles](https://discord.com/channels/689534383878701223/1133002668189700116/1134113997378027582)\n5.) [Serpent's Economy](https://discord.com/channels/689534383878701223/1133002668189700116/1134171819444805662)\n6.) [Leaving Punishments](https://discord.com/channels/689534383878701223/1133002668189700116/1134568608979234846)", color=0x47F599)

        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)
        await msg4.edit(content=f" ", embed=embed4)
        await msg5.edit(content=f" ", embed=embed5)
        await msg6.edit(content=f" ", embed=embed6)

        await lastmsg.edit(content=f" ", embed=lastembed)









    @Cog.listener('on_ready')
    async def server_info(self):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['server_info']) #? role change Channel

        msg1 = await ch.fetch_message(1052828325422317578) #? msg
        msg2 = await ch.fetch_message(1052828331197874176) #? msg
        msg3 = await ch.fetch_message(1052828335283122196) #? msg

        coin = self.bot.config['emotes']['coin']

        embed1=Embed(description=f"```fix\n█ SCP Server Info █\n```\n**SCP Server connect addresses**\n**Serpent's Garden [Alpha]** `n01.infra.serpents.garden:7777`\n**Serpent's Garden [Epsilon]** `n01.infra.serpents.garden:7778`\n**Serpent's Garden [Kappa]** `n01.infra.serpents.garden:7779`\n**Serpent's Garden [Theta]** `n01.infra.serpents.garden:7782`", color=0xFF0000)

        embed2=Embed(description=f"```fix\n█ Most Common Questions █\n```\n**Q: How can I see a comprehensive list off all the modded features on the servers?**\nA: <#1096531445792657439>\n\n**Q: How can I apply for staff?**\nA: <#1080592426965684255>\n\n**Q: How do I claim my in-game roles?**\nA:  [Click Here to sync your accounts to the servers](https://discord.com/api/oauth2/authorize?response_type=code&client_id=749684016550248490&scope=connections%20identify&redirect_uri=https://accounts.cedmod.nl/Auth/DiscordSSO&state=476547)\n\n**Q: How can I appeal my ban?**\nA: <#1080592426965684255>\n\n**Q: Are the plugins custom made?**\nA: Not all of them are custom made, but the best ones we have made by our dev who makes most of our plugins special & only for Serpent's Garden!\n\n**Q: Where can I see the server's player leaderboard**\nA: <#1052823837416357999>\n\n**Q: Where can I see a full report everything in a round?**\nA: <#1065409585764106321>", color=0x0000FF)

        embed3=Embed(title=f"**[- Coming Soon... -]**", 
        description=f"", color=0xFFFFFF)


        await msg1.edit(content=f" ", embed=embed1)
        await msg2.edit(content=f" ", embed=embed2)
        await msg3.edit(content=f" ", embed=embed3)







def setup(bot):
    x = rules_handler(bot)
    bot.add_cog(x)