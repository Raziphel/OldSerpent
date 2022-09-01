from utils.database import DatabaseConnection
import asyncpg

class Currency(object):
    all_currency = {}

    def __init__(self, user_id:int, coins:int=0, taxed:int=0, spent:int=0, paid:int=0):
        self.user_id = user_id
        self.coins = coins
        self.taxed = taxed
        self.spent = spent
        self.paid = paid

        self.all_currency[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO currency
                VALUES
                ($1, $2, $3, $4, $5)
                ''',
                self.user_id, self.coins, self.taxed, self.spent, self.paid
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE currency SET
                coins=$2, taxed=$3, spent=$4, paid=$5
                WHERE
                user_id=$1
                ''',
                self.user_id, self.coins, self.taxed, self.spent, self.paid
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_currency.get(user_id)
        if user == None:
            return cls(user_id)
        return user


    @classmethod
    def sort_coins(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_coins = sorted(cls.all_currency.values(), key=lambda u: u.coins, reverse=True)
        return sorted_coins


    @classmethod 
    def get_total_coins(cls):
        '''
        Gets all the user's collected amount of gold 
        '''
        total = 0
        for i in cls.all_currency.values():
            total += i.coins
        return total
