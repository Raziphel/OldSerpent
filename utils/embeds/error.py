
#* Discord
from discord import Embed
#* Additions
# from random import Choice

class ErrorEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #* Gets the varibles for the embed
        error_type = kwargs.pop('error_type', None)
        desc = kwargs.pop('desc', None)
        guild = kwargs.pop('guild', None)

        patron = self.bot.config['patreon']

        #! Make the embed
        super().__init__(*args, **kwargs)

        #* Add Color
        self.color = 0xdc143c #? Crimson

        #* Add title
        if error_type == "CommandNotFound":
            self.set_author(name=f"That's not a command!", url=patron)
    
        elif error_type == "MissingPermissions":
            self.set_author(name=f"I'm missing the permissions required!", url=patron)

        elif error_type == "CommandOnCooldown":
            self.set_author(name=f"That command is on cooldown!", url=patron)

        elif error_type == "InDmsCheckError":
            self.set_author(name=f"That command can only be ran in my dms!", url=patron)

        elif error_type == "MissingRequiredArgument":
            self.set_author(name=f"Command is missing required arguments!", url=patron)

        elif error_type == "BadArgument":
            self.set_author(name=f"Incorrect argument was given!", url=patron)

        elif error_type == "MissingError":
            self.set_author(name=f"[Bug Report] sent to developers!", url=patron)

        elif error_type == "UserCheckError":
            self.set_author(name=f"Only specific people can run that command!", url=patron)

        elif error_type == "DevCheckError":
            self.set_author(name=f"Only my developers can run that command!", url=patron)

        elif error_type == "GuildCheckError":
            self.set_author(name=f"That command belongs to a specific guild!", url=patron)

        elif error_type == "NSFWCheckError":
            self.set_author(name=f"This command only works in NSFW channels.", url=patron)

        elif error_type == "ModStaffCheckError":
            self.set_author(name=f"You must be atleast moderator to run this command.", url=patron)

        elif error_type == "AdminStaffCheckError":
            self.set_author(name=f"You must be Admin to run this command.", url=patron)

        else:
            self.set_author(name=f"An unknown error has occured.", url=patron)

        #* Add description
        if desc:
            self.description = desc

        #* Add footer
        self.set_footer(text=f"⚠ Error Message. ")
