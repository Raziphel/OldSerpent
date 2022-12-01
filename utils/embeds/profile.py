
# Discord
from discord import Embed, Member
from discord.ext.commands import command, Cog
# Utils
import utils
#Additions
from math import floor
from random import choice
from datetime import datetime as dt, timedelta

class ProfileEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #Gets the varibles for the embed
        type_ = kwargs.pop('type', None)
        user = kwargs.pop('user', Member)
        staff = kwargs.pop('staff', False)
        quick = kwargs.pop('quick', False)
        patron = self.bot.config['patreon']
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild

        # Make the embed
        super().__init__(*args, **kwargs)

        #! Define Varibles
        mod = utils.Moderation.get(user.id)
        lvl = utils.Levels.get(user.id)
        c = utils.Currency.get(user.id)
        tr = utils.Tracking.get(user.id)
        st = utils.Staff_Track.get(user.id)

        if type_ == 'Sfw_Sona':
            ch = utils.Sonas.get(user.id)
        elif type_ == 'Nsfw_Sona':
            ch = utils.Nsfw_sonas.get(user.id)

        #! Required xp
        if lvl.level == 0:
            requiredexp = 10
        elif lvl.level < 5:
            requiredexp = lvl.level*25
        else:
            requiredexp = round(lvl.level**2.25)

        #* Add Color
        self.color = tr.color

        #* Emojis
        coin = self.bot.config['emotes']['coin']
        safe = "<:SAFE:1020576690604343296>"
        euclid = "<:EUCLID:1020576687693496352>"
        keter = "<:KETER:1020576689245392937>"

        #! varibles
        joined_at = user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        guild = self.bot.get_guild(689534383878701223) #? Guild
        t1 = utils.DiscordGet(guild.roles, id=690037883821883421)
        t2 = utils.DiscordGet(guild.roles, id=704876369741480006)
        t3 = utils.DiscordGet(guild.roles, id=869140987392450620)
        t4 = utils.DiscordGet(guild.roles, id=1012179424940142613)
        support = "❌ Nota'Supporter"
        adult = None
        if t1 in user.roles:
            support = f"<:nitro:1012165382901092462> Nitro Booster"
        if t2 in user.roles:
            support = f"{safe} Safe Supporter"
        if t3 in user.roles:
            support = f"{euclid} Euclid Supporter"
        if t4 in user.roles:
            support = f"{keter} Keter Supporter"

        if mod.adult == True:
            if mod.child == False: 
                adult = "🔷 Verified Adult"
            else: adult = "🔶 Adult"
        if mod.adult == False:
            if mod.child == True:
                adult = "🔷 Verified Child"
            else: adult = "🔶 Child"



        #* Add author
        self.set_author(name=f"{user.name}'s {type_} Profile", icon_url=user.avatar.url, url=patron)

        #* Add the types feild
        if type_ == "Loading":
            self.add_field(name='Loading...', value=f":3", inline=True)

        #* Add author
        if type_ == "Default":
            self.add_field(name='📚 INFORMATION', value=f"**{adult}\n{support}**", inline=True)
            self.add_field(name='💸 VALUES', value=f"📈 Level: **{lvl.level:,}**\n***XP:*** {floor(lvl.exp):,}/**{requiredexp:,}**\n{coin} : **{floor(c.coins):,}x**", inline=True)
            self.add_field(name='🥇 RECORDS', value=f"✉ Messages: **{tr.messages:,}**\n🎤 VC Hours: **{floor(tr.vc_mins/60):,} ({floor((tr.vc_mins/60)/24):,} Days)**", inline=True)
            self.add_field(name='-', value=f"**Work In Progress**", inline=True)
            self.set_footer(text=f"Joined Razi's Realm: {joined_at}")

        if type_ == "Staff-Track":
            self.add_field(name='STAFF', value=f"❧ Mutes: {st.mutes}\n❧ Memes: {st.memes}\n❧ Nsfws: {st.nsfws}\n❧ Sonas: {st.mail_sonas}", inline=True)
            self.add_field(name='TRACK', value=f"❧ Purges: {st.purges}\n❧ Messages: {st.messages}\n❧ Monthly Msgs: {st.messages_month}\n❧ Verified: {st.mail_verification}", inline=True)
            if quick == False:
                self.set_footer(text=f"| 🔷 Main Profile |")

        if type_ == "Sfw_Sona":
            if staff == True:
                self.add_field(name='Name', value=f"{ch.name}", inline=True)
                self.add_field(name='Gender', value=f"{ch.gender}", inline=True)
                self.add_field(name='Age', value=f"{ch.age}", inline=True)
                self.add_field(name='Species', value=f"{ch.species}", inline=True)
                self.add_field(name='Likes', value=f"{ch.likes}", inline=True)
                self.color = ch.color
                self.set_footer(text=f"| sfw_sona |")
                if ch.bio != None:
                    self.add_field(name='Bio', value=ch.bio, inline=False)
                if ch.image != None:
                    self.set_image(url=ch.image)
            elif ch.verified == True:
                self.add_field(name='Name', value=f"{ch.name}", inline=True)
                self.add_field(name='Gender', value=f"{ch.gender}", inline=True)
                self.add_field(name='Age', value=f"{ch.age}", inline=True)
                self.add_field(name='Species', value=f"{ch.species}", inline=True)
                self.add_field(name='Likes', value=f"{ch.likes}", inline=True)
                self.color = ch.color
                if ch.bio != None:
                    self.add_field(name='Bio', value=ch.bio, inline=False)
                if ch.image != None:
                    self.set_image(url=ch.image)
                if quick == False:
                    self.set_footer(text=f"| 🔷 Main Profile |")
            else:
                self.add_field(name='Nothing?', value=f"❧ You don't have a verified sona!\n❧ Do `.setsona`", inline=True)
                if quick == False:
                    self.set_footer(text=f"| 🔷 Main Profile |")

        if type_ == "Nsfw_Sona":
            if staff == True:
                self.add_field(name='Name', value=f"{ch.name}", inline=True)
                self.add_field(name='Gender', value=f"{ch.gender}", inline=True)
                self.add_field(name='Age', value=f"{ch.age}", inline=True)
                self.add_field(name='Species', value=f"{ch.species}", inline=True)
                self.add_field(name='Likes', value=f"{ch.likes}", inline=True)
                self.color = ch.color
                self.set_footer(text=f"| nsfw_sona |")
                if ch.bio != None:
                    self.add_field(name='Bio', value=ch.bio, inline=False)
                if ch.image != None:
                    self.set_image(url=ch.image)
            elif ch.verified == True:
                self.add_field(name='Name', value=f"{ch.name}", inline=True)
                self.add_field(name='Gender', value=f"{ch.gender}", inline=True)
                self.add_field(name='Age', value=f"{ch.age}", inline=True)
                self.add_field(name='Species', value=f"{ch.species}", inline=True)
                self.add_field(name='Likes', value=f"{ch.likes}", inline=True)
                self.color = ch.color
                if ch.bio != None:
                    self.add_field(name='Bio', value=ch.bio, inline=False)
                if ch.image != None:
                    self.set_image(url=ch.image)
                if quick == False:
                    self.set_footer(text=f"| 🔷 Main Profile |")
            else:
                self.add_field(name='Nothing?', value=f"❧ You don't have a verified sona!\n❧ Do `.setsona`", inline=True)
                if quick == False:
                    self.set_footer(text=f"| 🔷 Main Profile |")
