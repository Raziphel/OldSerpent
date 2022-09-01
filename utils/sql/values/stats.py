from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Stats(object):
    all_stats = {}

    def __init__(self, user_id:int, location:str="Choose Start", health:int=100, mana:int=20, energy:int=10, armour:str="Loin Cloth", weapon:str="Fists", axe:str="None", rod:int="None"):
        self.user_id = user_id
        self.location = location
        self.health = health
        self.mana = mana
        self.energy = energy
        self.armour = armour
        self.weapon = weapon
        self.axe = axe
        self.rod = rod

        self.all_stats[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO stats
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ''',
                self.user_id, self.location, self.health, self.mana, self.energy, self.armour, self.weapon, self.axe, self.rod
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE stats SET
                location=$2, health=$3 mana=$4, energy=$5, armour=$6, weapon=$7, axe=$8, rod=$9
                WHERE
                user_id=$1
                ''',
                self.user_id, self.location, self.health, self.mana, self.energy, self.armour, self.weapon, self.axe, self.rod
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_stats.get(user_id)
        if user == None:
            return cls(user_id)
        return user
