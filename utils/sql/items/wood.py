from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Wood(object):
    all_wood = {}

    def __init__(self, user_id:int, oak:int=0, birch:int=0, spruce:int=0, mahogany:int=0, mystical:int=0, anima:int=0):
        self.user_id = user_id
        self.oak = oak
        self.birch = birch
        self.spruce = spruce
        self.mahogany = mahogany
        self.mystical = mystical
        self.anima = anima

        self.all_wood[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO wood
                VALUES
                ($1, $2, $3, $4, $5, $6, $7)
                ''',
                self.user_id, self.oak, self.birch, self.spruce, self.mahogany, self.mystical, self.anima
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE wood SET
                oak=$2, birch=$3 spruce=$4, mahogany=$5, mystical=$6, anima=$7
                WHERE
                user_id=$1
                ''',
                self.user_id, self.oak, self.birch, self.spruce, self.mahogany, self.mystical, self.anima
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_wood.get(user_id)
        if user == None:
            return cls(user_id)
        return user
