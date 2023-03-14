from utils.database import DatabaseConnection
import asyncpg

class Temp_Mute(object):
    all_temp_mute = {}

    def __init__(self, user_id:int, unmute_time:str):
        self.user_id = user_id
        self.unmute_time = unmute_time

        self.all_temp_mute[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO tempmute_timeout
                VALUES
                ($1, $2)
                ''',
                self.user_id, self.unmute_time
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE tempmute_timeout SET
                unmute_time=$2
                WHERE
                user_id=$1
                ''',
                self.user_id, self.unmute_time
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets table's connected varibles'''
        user = cls.all_temp_mute.get(user_id)
        if user == None:
            return cls(user_id)
        return user
