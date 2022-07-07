from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Miners(object):
    all_miners = {}

    def __init__(self, user_id:int, emerald:int=0, diamond:int=0, ruby:int=0, sapphire:int=0, amethyst:int=0, crimson:int=0):
        self.user_id = user_id
        self.sapphire = sapphire
        self.ruby = ruby
        self.emerald = emerald
        self.diamond = diamond
        self.amethyst = amethyst
        self.crimson = crimson

        self.all_miners[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO miners
                VALUES
                ($1, $2, $3, $4, $5, $6, $7)
                ''',
                self.user_id, self.emerald, self.diamond, self.ruby, self.sapphire, self.amethyst, self.crimson
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE miners SET
                emerald=$2, diamond=$3, ruby=$4, sapphire=$5, amethyst=$6, crimson=$7
                WHERE
                user_id=$1
                ''',
                self.user_id, self.emerald, self.diamond, self.ruby, self.sapphire, self.amethyst, self.crimson
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_miners.get(user_id)
        if user == None:
            return cls(user_id)
        return user

