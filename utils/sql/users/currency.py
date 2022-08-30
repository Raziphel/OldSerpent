from utils.database import DatabaseConnection
import asyncpg

class Currency(object):
    all_currency = {}

    def __init__(self, user_id:int, gold_coins:int=0, good_coins:int=0, evil_coins:int=0):
        self.user_id = user_id
        self.gold_coins = gold_coins
        self.good_coins = good_coins
        self.evil_coins = evil_coins

        self.all_currency[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO currency
                VALUES
                ($1, $2, $3, $4)
                ''',
                self.user_id, self.gold_coins, self.good_coins, self.evil_coins
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE currency SET
                gold_coins=$2, good_coins=$3, evil_coins=$4
                WHERE
                user_id=$1
                ''',
                self.user_id, self.gold_coins, self.good_coins, self.evil_coins
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_currency.get(user_id)
        if user == None:
            return cls(user_id)
        return user


    @classmethod
    def sort_gold_coins(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_coins = sorted(cls.all_currency.values(), key=lambda u: u.gold_coins, reverse=True)
        return sorted_coins


    @classmethod
    def sort_good_coins(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_coins = sorted(cls.all_currency.values(), key=lambda u: u.good_coins, reverse=True)
        return sorted_coins


    @classmethod
    def sort_evil_coins(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_coins = sorted(cls.all_currency.values(), key=lambda u: u.evil_coins, reverse=True)
        return sorted_coins


    @classmethod 
    def get_total_gold(cls):
        '''
        Gets all the user's collected amount of gold 
        '''
        total = 0
        for i in cls.all_currency.values():
            total += i.gold_coins
        return total


    @classmethod 
    def get_total_good(cls):
        '''
        Gets all the user's collected amount of good 
        '''
        total = 0
        for i in cls.all_currency.values():
            total += i.good_coins
        return total


    @classmethod 
    def get_total_evil(cls):
        '''
        Gets all the user's collected amount of evil
        '''
        total = 0
        for i in cls.all_currency.values():
            total += i.evil_coins
        return total
