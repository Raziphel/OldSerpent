from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Items(object):
    all_items = {}

    def __init__(self, user_id:int, thief_gloves:int=0, party_popper:int=0):
        self.user_id = user_id
        self.thief_gloves = thief_gloves
        self.party_popper = party_popper

        self.all_items[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO items
                VALUES
                ($1, $2, $3)
                ''',
                self.user_id, self.thief_gloves, self.party_popper
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE items SET
                thief_gloves=$2, party_popper=$3
                WHERE
                user_id=$1
                ''',
                self.user_id, self.thief_gloves, self.party_popper
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets table's connected varibles'''
        item = cls.all_items.get(user_id)
        if item == None:
            return cls(
                user_id = user_id,
                thief_gloves = 0,
                party_popper = 0,
            )
        return item
