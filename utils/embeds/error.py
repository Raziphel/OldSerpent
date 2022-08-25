
#* Discord
from discord import Embed
#* Additions
# from random import Choice

class ErrorEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #* Gets the varibles for the embed
        error_msg = kwargs.pop('error_msg', None)
        desc = kwargs.pop('desc', None)
        guild = kwargs.pop('guild', None)

        patron = self.bot.config['patreon']

        #! Make the embed
        super().__init__(*args, **kwargs)

        #* Add Color
        self.color = 0xdc143c #? Crimson

        #* Add title
        self.set_author(name=error_msg, url=patron)

        #* Add description
        if desc:
            self.description = desc

        #* Add footer
        self.set_footer(text=f"⚠ Error Message. ")
