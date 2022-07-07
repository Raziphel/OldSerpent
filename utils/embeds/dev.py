
#* Discord
from discord import Embed
#* Additions
# from random import Choice

class DevEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #* Gets the varibles for the embed
        title = kwargs.pop('title', None)
        desc = kwargs.pop('desc', None)
        guild = kwargs.pop('guild', None)

        #! Guild Checks
        if guild.id == self.bot.config['guilds']['FurryRoyaleID']:
            patron = self.bot.config['royale_patreon']
        else:
            patron = self.bot.config['razi_patreon']
        #! Make the embed
        super().__init__(*args, **kwargs)

        #* Add Color
        self.color = 0x1d89e3 #? Blue

        #* Add title
        if title:
            self.set_author(name=title, url=patron)

        #* Add description
        if desc:
            self.description = f"{desc}"

        #* Add footer
        self.set_footer(text=f"🌹 Developer Command")