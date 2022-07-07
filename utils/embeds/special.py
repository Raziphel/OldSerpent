
#* Discord
from discord import Embed
#* Additions
from random import randint, choice

import utils

class SpecialEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #* Gets the varibles for the embed
        title = kwargs.pop('title', None)
        desc = kwargs.pop('desc', None)
        thumbnail = kwargs.pop('thumbnail', None)
        footer = kwargs.pop('footer', None)
        guild = kwargs.pop('guild', None)


        #! Guild Checks
        if guild.id == self.bot.config['guilds']['FurryRoyaleID']:
            patron = self.bot.config['royale_patreon']
        else:
            patron = self.bot.config['razi_patreon']


        #! Make the embed
        super().__init__(*args, **kwargs)

        #* Add Color
        self.color = randint(1, 0xffffff) #? Random color

        #* Add title
        if title:
            self.set_author(name=title, url=patron)

        #* Add description
        if desc:
            self.description = desc

        if thumbnail:
            self.set_thumbnail(url=thumbnail)

        if footer:
            self.set_footer(text=footer)
        else:
            self.set_footer(text=choice(utils.Tips))
