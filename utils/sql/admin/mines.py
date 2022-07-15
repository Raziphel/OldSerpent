from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Mines(object):
    all_mines = {}

    def __init__(self, channel_id:int, last_msg:int=0, last_user:int=0, last_reward_type="silver", last_reward_amount=0):
        self.channel_id = channel_id
        self.last_msg = last_msg
        self.last_user = last_user
        self.last_reward_type = last_reward_type
        self.last_reward_amount = last_reward_amount

        self.all_mines[self.channel_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO mines
                VALUES
                ($1, $2, $3, $4, $5)
                ''',
                self.channel_id, self.last_msg, self.last_user, self.last_reward_type, self.last_reward_amount
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE mines SET
                last_msg=$2, last_user=$3, last_reward_type=$4, last_reward_amount=$5
                WHERE
                channel_id=$1
                ''',
                self.channel_id, self.last_msg, self.last_user, self.last_reward_type, self.last_reward_amount
            )

    @classmethod
    def get(cls, channel_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_mines.get(channel_id)
        if user == None:
            return cls(channel_id)
        return user

