
#* Discord
from discord import Embed
#* Additions
from random import randint

class QuestEmbed(Embed):

    bot = None

    def __init__(self, *args, **kwargs):
        #* Gets the varibles for the embed
        complete = kwargs.pop('complete', False)
        name = kwargs.pop('name', None)
        desc = kwargs.pop('desc', None)
        tip = kwargs.pop('tip', None)
        reward = kwargs.pop('reward', None)
        
        patron = self.bot.config['patreon']

        #! Make the embed
        super().__init__(*args, **kwargs)

        #* Add Color
        self.color = randint(1, 0xffffff) #? Random color

        #* Complete Quest
        if complete == True:
            self.set_author(name=f"- - QUEST COMPLETE - -", url=patron)
            self.description = f"You completed the quest: **{name}**\n\n{reward}"
        else:
            #* Add title
            self.set_author(name=f"QUEST: {name}", url=patron)

            #* Add description
            if desc:
                self.description = f"**DETAILS:** {desc}"

            #* Add footer
            self.set_footer(text=f"☘ TIP: {tip}")