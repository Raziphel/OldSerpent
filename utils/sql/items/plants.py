from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Plants(object):
    all_plants = {}

    def __init__(self, user_id:int, potato:int=0, carrot:int=0, wheat:int=0, dandelion:int=0, watermelon:int=0, catnip:int=0, marijuana:int=0):
        self.user_id = user_id
        self.potato = potato
        self.carrot = carrot
        self.wheat = wheat
        self.dandelion = dandelion
        self.watermelon = watermelon
        self.catnip = catnip
        self.marijuana = marijuana

        self.all_plants[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO plants
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8)
                ''',
                self.user_id, self.potato, self.carrot, self.wheat, self.dandelion, self.watermelon, self.catnip, self.marijuana
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE plants SET
                potato=$2, carrot=$3 wheat=$4, dandelion=$5, watermelon=$6, catnip=$7, marijuana=$8
                WHERE
                user_id=$1
                ''',
                self.user_id, self.potato, self.carrot, self.wheat, self.dandelion, self.watermelon, self.catnip, self.marijuana
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_plants.get(user_id)
        if user == None:
            return cls(user_id)
        return user
