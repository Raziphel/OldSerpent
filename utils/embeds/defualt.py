# Discord
from discord import Embed
from discord.ext.commands import command, Cog
from random import choice


import utils


class DefualtEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #* Gets the varibles for the embed
        user = kwargs.pop('user', None)
        title = kwargs.pop('author', None)
        thumbnail = kwargs.pop('thumbnail', None)
        image = kwargs.pop('image', None)
        desc = kwargs.pop('desc', None)
        patron = self.bot.config['patreon']


        #* Make the embed
        super().__init__(*args, **kwargs)

        #* Add Color
        if user:
            ss = utils.Settings.get(user.id)
            self.color = ss.color

        #* Add author
        if title:
            self.set_author(name=title, url=patron)

        #* Add thumbnail
        if thumbnail:
            self.set_thumbnail(url=thumbnail)

        #* Add image
        if image:
            self.set_image(url=image)
        if desc:
            self.description = f"{desc}"

        #* Add Footer
        emoji = choice(["🌷", "🌹", "🍃", "🌺", "🌼", "🌹", "'🥀"])
        self.set_footer(text=f"{emoji} {choice(utils.Tips)}")