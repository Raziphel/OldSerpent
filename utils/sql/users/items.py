from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Items(object):
    all_items = {}

    def __init__(self, user_id:int, thief_gloves:int=0, lot_tickets:int=0):
        self.user_id = user_id
        self.thief_gloves = thief_gloves
        self.lot_tickets = lot_tickets

        self.all_items[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO items
                VALUES
                ($1, $2, $3)
                ''',
                self.user_id, self.thief_gloves, self.lot_tickets
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE items SET
                thief_gloves=$2, lot_tickets=$3
                WHERE
                user_id=$1
                ''',
                self.user_id, self.thief_gloves, self.lot_tickets
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets table's connected varibles'''
        item = cls.all_items.get(user_id)
        if item == None:
            return cls(
                user_id = user_id,
                thief_gloves = 0,
                lot_tickets = 0,
            )
        return item


    @classmethod
    def sort_tickets(cls):
        '''sorts the user's by tickets. getting ranks!'''
        sorted_tickets = sorted(cls.all_items.values(), key=lambda u: u.lot_tickets, reverse=True)
        return sorted_tickets

    @classmethod 
    def get_total_tickets(cls):
        '''Gets total tickets'''
        total = 0
        for i in cls.all_items.values():
            total += i.lot_tickets
        return total