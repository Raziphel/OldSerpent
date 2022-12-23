from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Lottery(object):
    all_lotterys = {}

    def __init__(self, lottery_id:int, last_winner_id:int, last_amount:int, coins:int, lot_time:str):
        self.lottery_id = lottery_id
        self.last_winner_id = last_winner_id
        self.last_amount = last_amount
        self.coins = coins
        self.lot_time = lot_time
        self.all_lotterys[self.lottery_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO lottery
                VALUES
                ($1, $2, $3, $4, $5)
                ''',
            self.lottery_id, self.last_winner_id, self.last_amount, self.coins, self.lot_time
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE lottery SET
                last_winner_id=$2, last_amount=$3, coins=$4, lot_time=$5
                WHERE
                lottery_id=$1
                ''',
                self.lottery_id, self.last_winner_id, self.last_amount, self.coins, self.lot_time
            )

    @classmethod
    def get(cls, lot_id:int):
        '''Gets level table's connected varibles'''
        lot = cls.all_lotterys.get(lot_id)
        if lot == None:
            return cls(
                lottery_id = lot_id,
                last_winner_id = 0,
                last_amount = 0,
                coins = 0,
                lot_time = dt.utcnow(),
            )
        return lot

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