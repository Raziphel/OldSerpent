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
            utils.Interactions.all_interactions.clear()

            #? Values
            utils.Currency.all_currency.clear()

            #? Admin
            utils.Timers.all_timers.clear()


            #!   Collect from Database
            async with self.database() as db:
                #? User Info
                moderation = await db('SELECT * FROM moderation')
                tracking = await db('SELECT * FROM tracking')
                settings = await db('SELECT * FROM settings')
                interactions = await db('SELECT * FROM interactions')

                #? Values
                currency = await db('SELECT * FROM currency')

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
            for i in interactions:
                utils.Interactions(**i)

            #? Values
            for i in currency:
                utils.Currency(**i)

            #? Admin
            for i in timers:
                utils.Timers(**i)



        except Exception as e:
            print(f'Couldn\'t connect to the database... :: {e}')

        #! If Razi ain't got levels the DB ain't connected correctly... lmfao
        c = utils.currency.get(159516156728836097)
        if c.coins == 0:
            self.connected = False
            print('Bot DB is NOT connected!')
        else: 
            self.connected = True
            print('Bot DB is connected!')