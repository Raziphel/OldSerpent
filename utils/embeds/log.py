
#* Discord
from discord import Embed
#* Additions
from datetime import datetime as dt

class LogEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #* Gets the varibles for the embed
        type_ = kwargs.pop('type', None)
        title = kwargs.pop('title', None)
        desc = kwargs.pop('desc', None)
        thumbnail = kwargs.pop('thumbnail', None)
        footer = kwargs.pop('footer', None)


        #! Make the embed
        super().__init__(*args, **kwargs)

        #* Add Color
        if type_ == "change":
            self.color = 0xff00ff #? Fuscia
        elif type_ == "moderation":
            self.color = 0xff8000 #? Orange
        elif type_ == "negative":
            self.color = 0xdc143c #? Crimson
        elif type_ == "positive":
            self.color = 0x006400 #? Dark Green
        elif type_ == "special":
            self.color = 0xff7f50 #? Coral


        #* Add title
        if title:
            self.set_author(name=title)

        #* Add description
        if desc:
            self.description = f"{desc}"

        #* Add Thumbnail
        if thumbnail:
            self.set_thumbnail(url=thumbnail)

        #* Add footer
        if footer:
            self.set_footer(text=footer)
        else:
            self.set_footer(text=f"🔧 Log Embed") #! Put the date and time here, when your not being a bitch...