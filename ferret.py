import toml
import logging

from discord.ext import commands

import utils
from utils.database import DatabaseConnection


#! ------------------------- Ferret Main Class
class Ferret(commands.AutoShardedBot):
    def __init__(self, config_filename:str, *args, logger:logging.Logger=None, **kwargs):
        super().__init__(*args, fetch_offline_members=True, guild_subscriptions=True, **kwargs)

        self.logger = logger or logging.getLogger("Ferret")
        self.config_filename = config_filename
        self.config = None
        with open(self.config_filename) as z:
            self.config = toml.load(z)

        #! Adds all embeds to the Ferret Bot.
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
            utils.Levels.all_levels.clear()
            utils.Currency.all_currency.clear()
            utils.Moderation.all_moderation.clear()
            utils.Settings.all_settings.clear()
            utils.Timers.all_timers.clear()
            utils.Tracking.all_tracking.clear()
            utils.Mines.all_mines.clear()


            #!   Collect from Database
            async with self.database() as db:
                levels = await db('SELECT * FROM levels')
                currency = await db('SELECT * FROM currency')
                moderation = await db('SELECT * FROM moderation')
                settings = await db('SELECT * FROM settings')
                timers = await db('SELECT * FROM timers')
                tracking = await db('SELECT * FROM tracking')
                mines = await db('SELECT * FROM mines')


            #!   Cache all into local objects
            for i in levels:
                utils.Levels(**i)

            for i in currency:
                utils.Currency(**i)

            for i in moderation:
                utils.Moderation(**i)

            for i in settings:
                utils.Settings(**i)

            for i in timers:
                utils.Timers(**i)

            for i in tracking:
                utils.Tracking(**i)

            for i in mines:
                utils.Mines(**i)

        except Exception as e:
            print(f'Couldn\'t connect to the database... :: {e}')

        #! If Razi ain't got levels the DB ain't connected correctly... lmfao
        lvl = utils.Levels.get(159516156728836097)
        if lvl.level == 0:
            self.connected = False
            print('Bot DB is NOT connected!')
        else: 
            self.connected = True
            print('Bot DB is connected!')