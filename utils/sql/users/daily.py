from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Daily(object):
    all_dailys = {}

    def __init__(self, user_id:int, daily:int=0, last_daily:str=dt.utcnow(), premium:bool=False):
        self.user_id = user_id
        self.daily = daily
        self.last_daily = last_daily
        self.premium = premium

        self.all_dailys[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO daily
                VALUES
                ($1, $2, $3, $4)
                ''',
                self.user_id, self.last_daily, self.daily, self.premium
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE daily SET
                last_daily=$2, daily=$3, premium=$4
                WHERE
                user_id=$1
                ''',
                self.user_id, self.last_daily, self.daily, self.premium
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets daily table's connected varibles'''
        user = cls.all_dailys.get(user_id)
        if user == None:
            return cls(
                user_id = user_id,
                daily = 0,
                last_daily = dt.utcnow() - timedelta(days=5),
                premium = False,
            )
        return user
