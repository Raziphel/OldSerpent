
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
        user = kwargs.pop('user', Member)
        staff = kwargs.pop('staff', False)
        quick = kwargs.pop('quick', False)
        patron = self.bot.config['patreon']

        # Make the embed
        super().__init__(*args, **kwargs)

        #! Define Varibles
        lvl = utils.Levels.get(user.id) 
        ss = utils.Settings.get(user.id)
        tr = utils.Tracking.get(user.id)
        mod = utils.Moderation.get(user.id)
        c = utils.Currency.get(user.id)

        #* Required EXP varibles (Cant await in embeds...)
        if lvl.level == 0:
            requiredexp = 10
        elif lvl.level < 5:
            requiredexp = lvl.level*25
        else:
            requiredexp = round(lvl.level**2.25)

        #* get user's rank
        sorted_level_rank = utils.Levels.sort_levels()
        rank = sorted_level_rank.index(utils.Levels.get(user.id))

        #* Add Color
        self.color = ss.color

        #* Emojis
        goldcoin = "<:GoldCoin:1011145571240779817>"
        goodcoin = "<:GoodCoin:1011145572658446366>"
        evilcoin = "<:EvilCoin:1011145570112512051>"

        #! varibles
        joined_at = user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        guild = self.bot.get_guild(689534383878701223) #? Guild
        t1supporter = utils.DiscordGet(guild.roles, id=690037883821883421)
        t2supporter = utils.DiscordGet(guild.roles, id=704876369741480006)
        t3supporter = utils.DiscordGet(guild.roles, id=869140987392450620)
        t4supporter = utils.DiscordGet(guild.roles, id=1012179424940142613)
        support = "❌ Nota'Supporter"
        adult = None
        if t1supporter in user.roles:
            support = f"<:nitro:1012165382901092462> Tier I Supporter"
        if t2supporter in user.roles:
            support = f"{goldcoin} Tier II Supporter"
        if t3supporter in user.roles:
            support = f"{goodcoin} Tier III Supporter"
        if t4supporter in user.roles:
            support = f"{evilcoin} Tier IV Supporter"

        if mod.adult == True:
            if mod.child == False: 
                adult = "🔷 Verified Adult"
            else: adult = "🔶 Adult"
        if mod.adult == False:
            if mod.child == True:
                adult = "🔷 Verified Child"
            else: adult = "🔶 Child"
        

        #* Add author
        self.set_author(name=f"{user.name}'s Profile", icon_url=user.avatar.url, url=patron)
        self.add_field(name='📚 INFORMATION', value=f"**{adult}\n{support}**\n", inline=True)
        self.add_field(name='📊 LEVELING', value=f"🔶 Level Rank: **#{rank+1}**\n🔷 Level: **{lvl.level}**\n♦ Exp: **{floor(lvl.exp):,}/{requiredexp:,}**\n", inline=True)
        self.add_field(name='🥇 RECORDS', value=f"✉ Messages: **{tr.messages:,}**\n🎤 VC Hours: **{floor(tr.vc_mins/60):,} ({floor((tr.vc_mins/60)/24):,} Days)**", inline=True)
        self.add_field(name='💸 CURRENCY', value=f"{goldcoin} : **{floor(c.gold_coins):,}x**\n{goodcoin} : **{floor(c.good_coins):,}x**\n{evilcoin} : **{floor(c.evil_coins):,}x**", inline=True)
        self.add_field(name='-', value=f"**Work In Progress**", inline=True)
        self.set_footer(text=f"Joined Ferret's Palace: {joined_at}")
