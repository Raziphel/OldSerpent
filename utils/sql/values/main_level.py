from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Main_Level(object):
    all_levels = {}

    def __init__(self, user_id:int, level:int=0, exp:int=0, last_xp:str=dt.utcnow()):
        self.user_id = user_id
        self.level = level
        self.exp = exp
        self.last_xp = last_xp or dt.utcnow()

        self.all_levels[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO main_level
                VALUES
                ($1, $2, $3, $4, $5)
                ''',
                self.user_id, self.level, self.exp, self.last_xp
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE main_level SET
                level=$2, exp=$3, last_xp=$4
                WHERE
                user_id=$1
                ''',
                self.user_id, self.level, self.exp, self.last_xp
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