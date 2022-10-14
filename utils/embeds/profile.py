
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
        quick = kwargs.pop('quick', False)
        sona = kwargs.pop('sona', 1)
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild

        # Make the embed
        super().__init__(*args, **kwargs)

        #! Define Varibles
        ss = utils.Settings.get(user.id)
        tr = utils.Tracking.get(user.id)
        mod = utils.Moderation.get(user.id)
        c = utils.Currency.get(user.id)

        #* get user's rank
        sorted_level_rank = utils.Levels.sort_levels()
        rank = sorted_level_rank.index(utils.Levels.get(user.id))

        #* Add Color
        self.color = ss.color

        #* Emojis
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
        if t1supporter in user.roles:
            support = f"<:nitro:1012165382901092462> Nitro Booster"
        if t2supporter in user.roles:
            support = f"{safe} Safe Supporter"
        if t3supporter in user.roles:
            support = f"{euclid} Euclid Supporter"
        if t4supporter in user.roles:
            support = f"{keter} Keter Supporter"

        if mod.adult == True:
            if mod.child == False: 
                adult = "🔷 Verified Adult"
            else: adult = "🔶 Adult"
        if mod.adult == False:
            if mod.child == True:
                adult = "🔷 Verified Child"
            else: adult = "🔶 Child"


        #* Add Interactions
        if inte.premium == False:
            interact_gived = f"❧ Pats: **{inte.pats_given:,}**\n❧ Hugs: **{inte.hugs_given:,}**\n❧ Kisses: **{inte.kisses_given:,}**\n❧ Licks: **{inte.licks_given:,}**\n\n💤 **No premium!**"
            interact_received = f"❧ Pats: **{inte.pats_received:,}**\n❧ Hugs: **{inte.hugs_received:,}**\n❧ Kisses: **{inte.kisses_received:,}**\n❧ Licks: **{inte.licks_received:,}**"
        else:
            interact_gived = f"❧ Pats: **{inte.pats_given:,}**\n❧ Hugs: **{inte.hugs_given:,}**\n❧ Kisses: **{inte.kisses_given:,}**\n❧ Licks: **{inte.licks_given:,}**\n❧ Boops: **{inte.boops_given}**\n❧ Bites: **{inte.bites_given}**\n❧ Stabs: **{inte.stabs_given}**\n❧ Flirts: **{inte.flirts_given}**"
            interact_received = f"❧ Pats: **{inte.pats_received:,}**\n❧ Hugs: **{inte.hugs_received:,}**\n❧ Kisses: **{inte.kisses_received:,}**\n❧ Licks: **{inte.licks_received:,}**\n❧ Boops: **{inte.boops_received}**\n❧ Bites: **{inte.bites_received}**\n❧ Stabs: **{inte.stabs_received}**\n❧ Flirts: **{inte.flirts_received}**"


        #* Add author
        self.set_author(name=f"{user.name}'s {type_} Profile", icon_url=user.avatar_url, url=patron)

        #* Add the types feild
        if type_ == "Loading":
            self.add_field(name='Loading...', value=f":3", inline=True)

        #* Add author
        if type_ == "Default":
            self.add_field(name='📚 INFORMATION', value=f"**{adult}\n{support}**\n", inline=True)
            self.add_field(name='📊 LEVELING', value=f"🔶 Level Rank: **#{rank+1}**\n🔷 Level: **{lvl.level}**\n♦ Exp: **{floor(lvl.exp):,}/{requiredexp:,}**\n", inline=True)
            self.add_field(name='🥇 RECORDS', value=f"✉ Messages: **{tr.messages:,}**\n🎤 VC Hours: **{floor(tr.vc_mins/60):,} ({floor((tr.vc_mins/60)/24):,} Days)**", inline=True)
            self.add_field(name='💸 CURRENCY', value=f"{goldcoin} : **{floor(c.coins):,}x**\n{goodcoin} : **{floor(c.good_coins):,}x**\n{evilcoin} : **{floor(c.evil_coins):,}x**", inline=True)
            self.add_field(name='-', value=f"**Work In Progress**", inline=True)
            self.set_footer(text=f"Joined Razi's Realm: {joined_at}")

        if type_ == "Staff-Track":
            self.add_field(name='STAFF', value=f"❧ Mutes: {st.mutes}\n❧ Memes: {st.memes}\n❧ Nsfws: {st.nsfws}\n❧ Sonas: {st.mail_sonas}", inline=True)
            self.add_field(name='TRACK', value=f"❧ Purges: {st.purges}\n❧ Messages: {st.messages}\n❧ Monthly Msgs: {st.messages_month}\n❧ Verified: {st.mail_verification}", inline=True)
            if quick == False:
                self.set_footer(text=f"| 🔷 Main Profile |")

        if type_ == "Interactions":
            self.add_field(name='Given', value=interact_gived, inline=True)
            self.add_field(name='Received', value=interact_received, inline=True)
            if quick == False:
                self.set_footer(text=f"| 🔷 Main Profile |")

        if type_ == "Sona":
            if staff == True:
                self.add_field(name='Name', value=f"{ch.name}", inline=True)
                self.add_field(name='Gender', value=f"{ch.gender}", inline=True)
                self.add_field(name='Age', value=f"{ch.age}", inline=True)
                self.add_field(name='Species', value=f"{ch.species}", inline=True)
                self.add_field(name='Weight', value=f"{ch.weight}", inline=True)
                self.add_field(name='Height', value=f"{ch.height}", inline=True)
                self.set_footer(text=f"| {sona}_sona |")
                if ch.bio != None:
                    self.add_field(name='Bio', value=ch.bio, inline=False)
                if ch.image != None:
                    self.set_image(url=ch.image)
            elif ch.verified == True:
                self.add_field(name='Name', value=f"{ch.name}", inline=True)
                self.add_field(name='Gender', value=f"{ch.gender}", inline=True)
                self.add_field(name='Age', value=f"{ch.age}", inline=True)
                self.add_field(name='Species', value=f"{ch.species}", inline=True)
                self.add_field(name='Weight', value=f"{ch.weight}", inline=True)
                self.add_field(name='Height', value=f"{ch.height}", inline=True)
                if ch.bio != None:
                    self.add_field(name='Bio', value=ch.bio, inline=False)
                if ch.image != None:
                    self.set_image(url=ch.image)
                if quick == False:
                    self.set_footer(text=f"| 🔷 Main Profile |")
            else:
                self.add_field(name='Nothing?', value=f"❧ You don't have a verified character!\n❧ Do `.setsona`", inline=True)
                if quick == False:
                    self.set_footer(text=f"| 🔷 Main Profile |")
