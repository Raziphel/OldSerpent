from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Fish(object):
    all_fish = {}

    def __init__(self, user_id:int, salmon:int=0, cod:int=0, tuna:int=0, anglerfish:int=0, rainbow:int=0, pufferfish:int=0, swordfish:int=0, greatwhite:int=0, goldenfish:int=0, whale:int=0):
        self.user_id = user_id
        self.salmon = salmon
        self.cod = cod
        self.tuna = tuna
        self.anglerfish = anglerfish
        self.rainbow = rainbow
        self.pufferfish = pufferfish
        self.swordfish = swordfish
        self.greatwhite = greatwhite
        self.goldenfish = goldenfish
        self.whale = whale

        self.all_fish[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO fish
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ''',
                self.user_id, self.salmon, self.cod, self.tuna, self.anglerfish, self.rainbow, self.pufferfish, self.swordfish, self.greatwhite, self.goldenfish, self.whale
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE fish SET
                salmon=$2, cod=$3 tuna=$4, anglerfish=$5, rainbow=$6, pufferfish=$7, swordfish=$8, greatwhite=$9, goldenfish=$10, whale=$11
                WHERE
                user_id=$1
                ''',
                self.user_id, self.salmon, self.cod, self.tuna, self.anglerfish, self.rainbow, self.pufferfish, self.swordfish, self.greatwhite, self.goldenfish, self.whale,
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_fish.get(user_id)
        if user == None:
            return cls(user_id)
        return user
