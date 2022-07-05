from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Currency(object):
    all_currency = {}

    def __init__(self, user_id:int, sapphire:int=0, ruby:int=0, emerald:int=0, diamond:int=0, amethyst:int=0, crimson:int=0):
        self.user_id = user_id
        self.sapphire = sapphire
        self.ruby = ruby
        self.emerald = emerald
        self.diamond = diamond
        self.amethyst = amethyst
        self.crimson = crimson

        self.all_currency[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO currency
                VALUES
                ($1, $2, $3, $4, $5, $6, $7)
                ''',
                self.user_id, self.sapphire, self.ruby, self.emerald, self.diamond, self.amethyst, self.crimson
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE currency SET
                sapphire=$2, ruby=$3, emerald=$4, diamond=$5, amethyst=$6, crimson=$7
                WHERE
                user_id=$1
                ''',
                self.user_id, self.sapphire, self.ruby, self.emerald, self.diamond, self.amethyst, self.crimson
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_currency.get(user_id)
        if user == None:
            return cls(user_id)
        return user

    @classmethod
    def sort_emeralds(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_emeralds = sorted(cls.all_currency.values(), key=lambda u: u.emerald, reverse=True)
        return sorted_emeralds

    @classmethod
    def sort_diamonds(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_diamonds = sorted(cls.all_currency.values(), key=lambda u: u.diamond, reverse=True)
        return sorted_diamonds

    @classmethod
    def sort_ruby(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_rubys = sorted(cls.all_currency.values(), key=lambda u: u.ruby, reverse=True)
        return sorted_rubys

    @classmethod
    def sort_sapphire(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_sapphires = sorted(cls.all_currency.values(), key=lambda u: u.sapphire, reverse=True)
        return sorted_sapphires