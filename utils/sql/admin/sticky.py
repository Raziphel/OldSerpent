from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Sticky(object):
    all_stickys = {}

    def __init__(self, channel_id:int, message_id:int):
        self.channel_id = channel_id
        self.message_id = message_id
        self.all_stickys[self.channel_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO sticky
                VALUES
                ($1, $2)
                ''',
            self.channel_id, self.message_id
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE sticky SET
                message_id=$2
                WHERE
                channel_id=$1
                ''',
                self.channel_id, self.message_id
            )

    @classmethod
    def get(cls, lot_id:int):
        '''Gets level table's connected varibles'''
        message = cls.all_stickys.get(lot_id)
        if message == None:
            return cls(
                channel_id = lot_id,
                message_id = 0,
            )
        return message

    # @classmethod
    # def sort_levels(cls):
    #     '''sorts the user's by balance. getting ranks!'''
    #     sorted_levels = sorted(cls.all_levels.values(), key=lambda u: u.level, reverse=True)
    #     return sorted_levels

    # @classmethod 
    # def get_total_levels(cls):
    #     '''Gets all the user's collected levels'''
    #     total = 0
    #     for i in cls.all_levels.values():
    #         total += i.level
    #     return total

    # @classmethod 
    # def get_total_users(cls):
    #     '''Gets all the user's collected.'''
    #     total = 0
    #     for i in cls.all_levels.values():
    #         total += 1
    #     return total