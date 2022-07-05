
# Discord
from discord import Embed, Member
from discord.ext.commands import command, Cog
# Utils
import utils
#Additions
from math import floor
from random import choice

class ProfileEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #Gets the varibles for the embed
        type_ = kwargs.pop('type', None)
        user = kwargs.pop('user', Member)
        staff = kwargs.pop('staff', False)
        quick = kwargs.pop('quick', False)

        # Make the embed
        super().__init__(*args, **kwargs)


        #! Define Varibles
        lvl = utils.Levels.get(user.id) 
        ss = utils.Settings.get(user.id)
        mod = utils.Moderation.get(user.id)
        c = utils.Currency.get(user.id)
        tr = utils.Tracking.get(user.id)
        me = utils.Miners.get(user.id)

        #* Required EXP varibles (Cant await in embeds...)
        if lvl.level == 0:
            requiredexp = 10
        elif lvl.level < 5:
            requiredexp = lvl.level*25
        else:
            requiredexp = round(lvl.level**2.25)

        #* Setup the emoji names
        emerald = self.bot.config['emotes']['emerald']
        diamond = self.bot.config['emotes']['diamond']
        ruby = self.bot.config['emotes']['ruby']
        sapphire = self.bot.config['emotes']['sapphire']
        amethyst = self.bot.config['emotes']['amethyst']
        crimson = self.bot.config['emotes']['crimson']


        #? get user's rank
        sorted_level_rank = utils.Levels.sort_levels()
        rank = sorted_level_rank.index(utils.Levels.get(user.id))
        
        #? Generate prestige messages
        if lvl.prestige is None:
            prestige = "**Not yet prestiged**"
        else:
            prestige = f"❧ Prestige: **{lvl.prestige}x**"

        #* Add Color
        self.color = ss.color

        #* Add author
        self.set_author(name=f"{user.name}'s {type_} Profile", icon_url=user.avatar.url, url=self.bot.config['patreon'])

        #* Add the types feild
        if type_ == "Loading":
            self.add_field(name='Loading...', value=f":3", inline=True)

        if type_ == "Default":
            self.add_field(name='LEVELING', value=f"❧ Ranking: **#{rank+1}**\n{prestige}\n❧ Level: **{lvl.level}**\n❧ Exp: **{floor(lvl.exp):,}/{requiredexp:,}**\n", inline=True)
            self.add_field(name='STATISTICS', value=f"❧ Adult?: **{mod.adult}**\n❧ Messages: **{tr.messages:,}**\n❧ VC Hours: **{floor(tr.vc_mins/60):,}**", inline=True)
            self.set_footer(text=f"| 💸 Gems | ⛏ Miners |")


        if type_ == "Currency":
            self.description = f"**CURRENCY**\n\n❧ {emerald} : **{floor(c.emerald):,}x**\n❧ {diamond} : **{floor(c.diamond):,}x**\n❧ {ruby} : **{floor(c.ruby):,}x**\n❧ {sapphire} : **{floor(c.sapphire):,}x**\n❧ {amethyst} : **{floor(c.amethyst):,}x**\n❧ {crimson} : **{floor(c.crimson):,}x**"
            if quick == False:
                self.set_footer(text=f"| 🔷 Return |")

        if type_ == "Miners":
            self.description = f"**MINERS**\n\n❧ {emerald} : **{me.emerald:,}/10**\n❧ {diamond} : **{me.diamond:,}/9**\n❧ {ruby} : **{me.ruby:,}/8**\n❧ {sapphire} : **{me.sapphire:,}/7**\n❧ {amethyst} : **{me.amethyst:,}/6**\n❧ {crimson} : **{me.crimson:,}/5**"
            if quick == False:
                self.set_footer(text=f"| 🔷 Return |")

