import toml
import logging

from discord.ext import commands

import utils
from utils.database import DatabaseConnection


#! ------------------------- Serpent Main Class
class Serpent(commands.AutoShardedBot):
    def __init__(self, config_filename:str, *args, logger:logging.Logger=None, **kwargs):
        super().__init__(*args, fetch_offline_members=True, guild_subscriptions=True, **kwargs)

        self.logger = logger or logging.getLogger("Serpent")
        self.config_filename = config_filename
        self.config = None
        with open(self.config_filename) as z:
            self.config = toml.load(z)

        #! Adds all embeds to the Serpent Bot.
        utils.DefualtEmbed.bot = self
        utils.SpecialEmbed.bot = self
        utils.LogEmbed.bot = self
        utils.DevEmbed.bot = self
        utils.ProfileEmbed.bot = self
        utils.ErrorEmbed.bot = self
        utils.MailEmbed.bot = self
        utils.WarningEmbed.bot = self

        #! Load Functions
        utils.UserFunction.bot = self

        self.database = DatabaseConnection
        self.database.config = self.config['database']
        self.startup_method = None
        self.connected = False



    def run(self):
        
        self.startup_method = self.loop.create_task(self.startup())
        super().run(self.config['token'])


    async def startup(self):
        """Load database"""

        try: 
            #? Try this to prevent reseting the database on accident!
            #! Clear cache
            #? User Info
            utils.Moderation.all_moderation.clear()
            utils.Tracking.all_tracking.clear()
            utils.Settings.all_settings.clear()

            #? Values
            utils.Main_Level.all_levels.clear()
            utils.Currency.all_currency.clear()
            utils.Quests.all_quests.clear()
            utils.Skill_Level.all_levels.clear()
            utils.Stats.all_stats.clear()

            #? Items
            utils.Fish.all_fish.clear()
            utils.Ores.all_ores.clear()
            utils.Plants.all_plants.clear()
            utils.Wood.all_wood.clear()

            #? Admin
            utils.Timers.all_timers.clear()


            #!   Collect from Database
            async with self.database() as db:
                #? User Info
                moderation = await db('SELECT * FROM moderation')
                tracking = await db('SELECT * FROM tracking')
                settings = await db('SELECT * FROM settings')

                #? Values
                main_level = await db('SELECT * FROM main_level')
                currency = await db('SELECT * FROM currency')
                stats = await db('SELECT * FROM stats')
                skill_level = await db('SELECT * FROM skill_level')
                quests = await db('SELECT * FROM quests')

                #? Items
                fish = await db('SELECT * FROM fish')
                ores = await db('SELECT * FROM ores')
                plants = await db('SELECT * FROM plants')
                wood = await db('SELECT * FROM wood')

                #? Admin
                timers = await db('SELECT * FROM timers')


            #!   Cache all into local objects
            #? User Info
            for i in moderation:
                utils.Moderation(**i)
            for i in settings:
                utils.Settings(**i)
            for i in tracking:
                utils.Tracking(**i)

            #? Values
            for i in main_level:
                utils.Main_Level(**i)
            for i in currency:
                utils.Currency(**i)
            for i in stats:
                utils.Stats(**i)
            for i in skill_level:
                utils.Skill_Level(**i)
            for i in quests:
                utils.Quests(**i)

            #? Items
            for i in fish:
                utils.Fish(**i)
            for i in ores:
                utils.Ores(**i)
            for i in plants:
                utils.Plants(**i)
            for i in wood:
                utils.Wood(**i)

            #? Admin
            for i in timers:
                utils.Timers(**i)



        except Exception as e:
            print(f'Couldn\'t connect to the database... :: {e}')

        #! If Razi ain't got levels the DB ain't connected correctly... lmfao
        lvl = utils.Main_Level.get(159516156728836097)
        if lvl.level == 0:
            self.connected = False
            print('Bot DB is NOT connected!')
        else: 
            self.connected = True
            print('Bot DB is connected!')