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
        utils.CoinFunctions.bot = self

        self.database = DatabaseConnection
        self.database.config = self.config['database']
        self.startup_method = None
        self.connected = False

        #! Supporters
        self.donators = ["🔥 Supporter II 🔥", "🔱 Supporter  III🔱"]


    def run(self):
        
        self.startup_method = self.loop.create_task(self.startup())
        super().run(self.config['token'])


    async def startup(self):
        """Load database"""

        try:   #? Try this to prevent reseting the database on accident!
            #! Clear cache
            utils.Moderation.all_moderation.clear()
            utils.Levels.all_levels.clear()
            utils.Currency.all_currency.clear()
            utils.Sonas.all_sonas.clear()
            utils.Nsfw_sonas.all_nsfw_sonas.clear()
            utils.Timers.all_timers.clear()
            utils.Tracking.all_tracking.clear()
            utils.Staff_Track.all_staff_track.clear()


            #!   Collect from Database
            async with self.database() as db:
                moderation = await db('SELECT * FROM moderation')
                levels = await db('SELECT * FROM levels')
                currency = await db('SELECT * FROM currency')
                sonas = await db('SELECT * FROM sonas')
                nsfw_sonas = await db('SELECT * FROM nsfw_sonas')
                timers = await db('SELECT * FROM timers')
                tracking = await db('SELECT * FROM tracking')
                staff_track = await db('SELECT * FROM staff_track')

            #!   Cache all into local objects
            for i in moderation:
                utils.Moderation(**i)

            for i in levels:
                utils.Levels(**i)

            for i in currency:
                utils.Currency(**i)

            for i in sonas:
                utils.Sonas(**i)

            for i in nsfw_sonas:
                utils.Nsfw_sonas(**i)

            for i in timers:
                utils.Timers(**i)

            for i in tracking:
                utils.Tracking(**i)

            for i in staff_track:
                utils.Staff_Track(**i)



        except Exception as e:
            print(f'Couldn\'t connect to the database... :: {e}')


        #! If Razi ain't got coins the DB ain't connected correctly... lmfao
        lvl = utils.Levels.get(159516156728836097)
        if lvl.level == 0:
            self.connected = False
            print('Bot database is NOT connected!')
        else: 
            self.connected = True
            print('Bot database is connected!')