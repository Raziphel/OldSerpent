from utils.database import DatabaseConnection
import asyncpg

class Currency(object):
    all_currency = {}

    def __init__(self, user_id:int, silver:int=0, gold:int=0, diamond:int=0, emerald:int=0, ruby:int=0, sapphire:int=0, amethyst:int=0, phelstone:int=0):
        self.user_id = user_id
        self.silver = silver
        self.gold = gold
        self.diamond = diamond
        self.emerald = emerald
        self.ruby = ruby
        self.sapphire = sapphire
        self.amethyst = amethyst
        self.phelstone = phelstone

        self.all_currency[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO currency
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ''',
                self.user_id, self.silver, self.gold, self.diamond, self.amethyst, self.ruby, self.sapphire, self.emerald, self.phelstone
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE currency SET
                silver=$2, gold=$3, diamond=$4, emerald=$5, ruby=$6, sapphire=$7, amethyst=$8, phelstone=$9
                WHERE
                user_id=$1
                ''',
                self.user_id, self.silver, self.gold, self.diamond, self.emerald, self.sapphire, self.ruby, self.amethyst, self.phelstone
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_currency.get(user_id)
        if user == None:
            return cls(user_id)
        return user
