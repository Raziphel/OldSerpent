from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Tracking(object):
    all_tracking = {}

    def __init__(self, user_id:int, messages:int=0, vc_mins:int=0, last_image:str=dt.now()):
        self.user_id = user_id
        self.messages = messages
        self.vc_mins = vc_mins
        self.last_image = last_image

        self.all_tracking[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO tracking
                VALUES
                ($1, $2, $3, $4)
                ''',
                self.user_id, self.messages, self.vc_mins, self.last_image
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE tracking SET
                messages=$2, vc_mins=$3, last_image=$4
                WHERE
                user_id=$1
                ''',
                self.user_id, self.messages, self.vc_mins, self.last_image
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_tracking.get(user_id)
        if user == None:
            return cls(user_id)
        return user
