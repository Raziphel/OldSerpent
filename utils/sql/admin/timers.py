from utils.database import DatabaseConnection
import asyncpg

from datetime import datetime as dt, timedelta


class Timers(object):
    all_timers = {}

    def __init__(self, guild_id:int, last_nitro_reward:str):
        self.guild_id = guild_id
        self.last_nitro_reward = last_nitro_reward

        self.all_timers[self.guild_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO timers
                VALUES
                ($1, $2)
                ''',
                self.guild_id, self.last_nitro_reward
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE timers SET
                last_nitro_reward=$2
                WHERE
                guild_id=$1
                ''',
                self.guild_id, self.last_nitro_reward
            )

    @classmethod
    def get(cls, guild_id:int):
        '''Gets table's connected varibles'''
        guild = cls.all_timers.get(guild_id)
        if guild is None:
            return cls(
                guild_id=guild_id,
                last_nitro_reward=(dt.now()-timedelta(days=50))
            )
        return guild
