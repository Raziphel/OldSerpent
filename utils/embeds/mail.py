# Discord
from discord import Embed, Member
from discord.ext.commands import command, Cog

import utils

from random import choice

class MailEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #Gets the varibles for the embed
        message = kwargs.pop('message', None)
        color = kwargs.pop('color', None)
        title = kwargs.pop('title', None)
        footer = kwargs.pop('footer', None)
        author = kwargs.pop('author', Member)
        image = kwargs.pop('image', None)

        # Make the embed
        super().__init__(*args, **kwargs)

        # Define color:
        self.color = color
        
        # Set embed footer
        self.set_footer(text=footer)

        # Set embed setup
        self.set_author(name=title, icon_url=author.avatar.url)

        # Set description
        self.description = message
        
        if image != None:
            self.set_image(url=image)
