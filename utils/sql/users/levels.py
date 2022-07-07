from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Levels(object):
    all_levels = {}

    def __init__(self, user_id:int, level:int=0, exp:int=0, last_xp:str=dt.utcnow(), prestige:int=0):
        self.user_id = user_id
        self.level = level
        self.exp = exp
        self.last_xp = last_xp or dt.utcnow()
        self.prestige = prestige

        self.all_levels[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO levels
                VALUES
                ($1, $2, $3, $4, $5)
                ''',
                self.user_id, self.level, self.exp, self.last_xp, self.prestige
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE levels SET
                level=$2, exp=$3, last_xp=$4, prestige=$5
                WHERE
                user_id=$1
                ''',
                self.user_id, self.level, self.exp, self.last_xp, self.prestige
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_levels.get(user_id)
        if user == None:
            return cls(user_id)
        return user

    @classmethod
    def sort_levels(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_levels = sorted(cls.all_levels.values(), key=lambda u: u.level, reverse=True)
        return sorted_levels