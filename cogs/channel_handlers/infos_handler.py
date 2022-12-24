
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

        embed2=Embed(title=f"**[- SCP Servers -]**", 
        description=f"**If you are looking for information related SCP servers check #server-info for most things you'd meed!**\n\nThis will be updated soon.", color=0x47F599)

        embed3=Embed(title=f"**[- The 05 Council -]**", 
        description=f"The 05 Council are the formal Administrators of the server!  Where as the The Red Right Hand is a form of moderators for the server!  The 05 council is never open to applications, but the Red Right Hand and Nine Tailed Fox always are.", color=0xF5AE47)

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
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        ch = guild.get_channel(self.bot.config['channels']['role_change']) #? role change Channel

        msg1 = await ch.fetch_message(1029973755428093986) #? msg
        msg2 = await ch.fetch_message(1029973761673408543) #? msg
        msg3 = await ch.fetch_message(1029973773656531015) #? msg
        msg4 = await ch.fetch_message(1029975810251169873) #? msg
        
        coin = self.bot.config['emotes']['coin']

        embed1=Embed(title=f"**[- Level Roles -]**", 
        description=f"This is the levels you recieve each role at! Any other roles are probably staff or a donator role!\n\n**Level 100 ->** `Serpent's Hand`\n**Level 90 ->** `Gamers Against Weed`\n**Level 80 ->** `Chaos Insurgency`\n**Level 75 ->** `Children of the Scarlet King`\n**Level 70 ->** `Sarkic Cult`\n**Level 65 ->** `Church of the Broken God`\n**Level 60 ->** `Global Occult Coalition`\n**Level 55 ->** `Unusual Incidents Unit`\n**Level 50 ->** `Ethics Committee`\n**Level 45 ->** `Memetics Division`\n**Level 40 ->** `Site Director`\n**Level 35 ->** `Facility Manager`\n**Level 30 ->** `MTF Operative`\n**Level 25 ->** `Sequrity Officer`\n**Level 20 ->** `Containment Specialist`\n**Level 15 ->** `Head-Reseracher`\n**Level 10 ->** `Scientist`\n**Level 5 ->** `D-Class`\n**Level 0 ->** `Janitor`", color=0xFF0000)

        embed2=Embed(title=f"**[- Coming Soon -]**", 
        description=f"", color=0x0000FF)

        embed3=Embed(title=f"**[- Update Pings -]**", 
        description=f"**These roles are pinged by staff only.  Anyone who pings the role will be banned.** *So atleast if ya do get pinged and its not staff! Ya get to see someone banned! :)*\n\n🔔 `Discord Pings`\nThese are pings focused towards the Discord Server!.\n\n🧪 `Server Pings`\nThese are pings focused towards the SCP Servers!. ", color=0xFFFFFF)

        embed4=Embed(title=f"**[- Pickable Roles -]**", 
        description=f"**These roles are permenant will require DMing or pinging 05 Council to change.**\n\n🚬 `Adult`\nThis will give you access to any NSFW marked channels in any category on the server.  Your other roles automatically update to adult versions.\n\n🍺 `Adult?`\nThis will give you access to VC channels that only Adults can join.\nYou will not have access to the NSFW text channels.\n\n🍼 `Child`\nThis will let the mark you as a child.\nIt is encouraged to get and not lie.\n\n🐾 `Furry`\nThis role is for those degenerates\n\n🏹 `Kingussy`\nThis is for certian specific people.  You must be invited and have a password.", color=0xFF00FF)

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
        description=f"**SCP Server connect addresses**\nSerpent's Garden #1 `n01.infra.serpents.garden:7777`\nSerpent's Garden #2 `n01.infra.serpents.garden:7778`\nSerpent's Garden #3 `n01.infra.serpents.garden:7779`\n\n**Permission Role Sync:** [Click Me](https://serpents_garden.cmod.app) (Will have to sync your Steam and Discord)\n*The following site is used to sync your roles on Discord to the SCP server!  All staff, nitro boosters and supporters will need to go here to get their roles synced to the SCP servers!*\n\n**Were you banned from the server?**\nYou can make an appeal here: [Click Me](https://serpents_garden.cmod.app) (Will have to sync your Steam and Discord)", color=0xFF0000)

        embed2=Embed(title=f"**[- SCP Plugin List -]**", 
        description=f"**This is a list of the plugins currently running on the SCP Serpent's Garden Server!**\n\n**Permission Systems**\nThis is just a plugin for syncing roles on the Discord Server.", color=0x0000FF)

        embed3=Embed(title=f"**[- Coming Soon -]**", 
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
        elif emoji == "🧪":
            updates = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['server_updates'])
            await member.add_roles(updates, reason="Will get updates now.")
        elif emoji == "🔔":
            updates = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['discord_updates'])
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