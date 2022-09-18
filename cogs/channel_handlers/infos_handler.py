
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
        description=f"**This is probably important by the way!**\n\n**1.)** Respect Everyone, not a single person doesn't deserve respect, especially the 05 Council.\n\n**2.)** Harrassment, Bully, Attacking of any kind or form of any member on this server isnt allowed. Period.\n\n**3.)** Drama, most people here have already gone through highschool, don't bring it back.\n\n**4.)** ENGLISH.  This is an American server you will be expected to only speak english or not speak at all.\n\n**5.)** Common Sense, Don't be annoying or do anything that would make a 05 Council have to punish. (Should be easy.)\n\n**6.)** Discord TOS, obviously don't do anything discord already doesn't allow, could count as previous rule.\n\n**7.)** Accepting the chaos and rules presented by The Serpent.", color=0xF54747)

        embed2=Embed(title=f"**[- The Serpent's Game -]**", 
        description=f"**1.)** To move between areas you must use <#997346872622596136>!\n\n**2.)** Interactions with The Serpent, sending messages and being in VC will all level you up!\n\n**3.)** Getting a better role requires higher levels.\n\n**4.)** The 05 Council must use Alpha-1 to participate in my game.\n\n**5.)** When you die in my game you are moved to a Dead Area for a few hours.  Leaving open your role slot.\n\n**6.)** The Serpent's Hand can veiw the Serpent's server's logs...\n\n**7.)** For in depth information go to <#1020959150890565703>", color=0x47F599)

        embed3=Embed(title=f"**[- The 05 Council -]**", 
        description=f"The <@891793700932431942> is the Discord Server's form of Staff.  They are the only Role on the server that are **Omni-Present**. (meaning they do not have to travel between zones)\n\n**The 05 are also not allowed to interact with The Serpent like regular users.**\n\nThe <@1020893519885373450> use The Serpent normally, being the 05's only way for presence in \"The Game\".\n\nThe 05 Council's corresponding number is in order of rank.", color=0xF5AE47)

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
        ch = guild.get_channel(self.bot.config['channels']['verify']) #? Rules Channel

        msg1 = await ch.fetch_message(1011068499495497748) #? msg
        msg2 = await ch.fetch_message(1011068510320992325) #? msg
        msg3 = await ch.fetch_message(1011068526028660787) #? msg

        embed1=Embed(title=f"**[- Age Verification -]**", 
        description=f"**To gain access to the adult channels, which are not NSFW focused.**\n\n*(You will have to be accepted by the council via verification)*\n🔥 `Adult Verification`\n❧ Gives NSFW access for any section you are apart of.\n\n💦 `Kinda Adult Verification`\n❧ Marked as Adult but no NSFW text/image channel access.\n\n🎈 `Underage`\n❧ Marks you as a child and keeps you safe!\n❧ Lying about your age never pays off.", color=0xD047F5)

        embed2=Embed(title=f"**[- Constant Access -]**", 
        description=f"**Razi's Realm has multiple different sections to it!**\nYou may not want access to all these different sections.  So you can simply choose what you would like to have access to, using this handler!\n\n*Channels have very different permissions (Ex: Posting Images) depending on what they're about.*\n\n**These are channels more related to Razi, could be the server's main channels!**\n\n*( You will have to agree to rules in verification. )*\n🎀 `Razi's Lounge`\n❧ This gives you access to Razi's General channels!\n❧ Permissions require <#946730953731100682> purchases.\n\n📚 `Wander's Library`\n❧ This gives you access to all of the Server's Logs.\n❧ Channels are read only and Adult Logs only visible by adults.\n**Now requires purchase from <#946730953731100682>**.", color=0x47D0F5)

        embed3=Embed(title=f"**[- Secondary Channel Access -]**", 
        description=f"*(You will have to be accepted by the council via verification)*\n🏹 `Kingussy Brothers`\n❧ This is for those who apart of the Kingussy alliance!\n❧ This requires a password only Ussy brothers would know.\n\n🧸 `SCP Fanatic`\n❧ This is for the SCP fanatics.\n❧ Has information for the *SCP:Secret Labratory* server information.\n❧ Permissions require <#946730953731100682> purchases.\n❧ Doesn't require verification.\n\n🐾 `Furry`\n❧ This is for the people into furry art and hangin' with other furfags.\n❧ No RP/ERP.\n❧ No flirting/dating.\n❧ No being a cringe lord.", color=0x4799F5)

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