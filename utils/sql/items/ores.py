from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Ores(object):
    all_ores = {}

    def __init__(self, user_id:int, coal:int=0, copper:int=0, tin:int=0, iron:int=0, silver:int=0, gold:int=0, tungsten:int=0, platinum:int=0, mithril:int=0, phelgem:int=0):
        self.user_id = user_id
        self.coal = coal
        self.copper = copper
        self.tin = tin
        self.iron = iron
        self.silver = silver
        self.gold = gold
        self.tungsten = tungsten
        self.platinum = platinum
        self.mithril = mithril
        self.phelgem = phelgem

        self.all_ores[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO ores
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ''',
                self.user_id, self.coal, self.copper, self.tin, self.iron, self.silver, self.gold, self.tungsten, self.platinum, self.mithril, self.phelgem
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE ores SET
                coal=$2, copper=$3 tin=$4, iron=$5, silver=$6, gold=$7, tungsten=$8, platinum=$9, mithril=$10, phelgem=$11
                WHERE
                user_id=$1
                ''',
                self.user_id, self.coal, self.copper, self.tin, self.iron, self.silver, self.gold, self.tungsten, self.platinum, self.mithril, self.phelgem,
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_ores.get(user_id)
        if user == None:
            return cls(user_id)
        return user
