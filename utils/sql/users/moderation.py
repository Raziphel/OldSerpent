from utils.database import DatabaseConnection
import asyncpg

class Moderation(object):
    all_users_moderation = {}

    def __init__(self, user_id:int, prisoner:bool=False, gagged:bool=False, violations:int=0, nsfw:bool=False, memes:int=0):
        self.user_id = user_id
        self.prisoner = prisoner
        self.gagged = gagged
        self.violations = violations
        self.nsfw = nsfw
        self.memes = memes

        self.all_users_moderation[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO moderation
                VALUES
                ($1, $2, $3, $4, $5, $6)
                ''',
                self.user_id, self.prisoner, self.gagged, self.violations, self.nsfw, self.memes
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE moderation SET
                prisoner=$2, gagged=$3, violations=$4, nsfw=$5, memes=$6
                WHERE
                user_id=$1
                ''',
                self.user_id, self.prisoner, self.gagged, self.violations, self.nsfw, self.memes
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets channel table's connected varibles'''
        user = cls.all_users_moderation.get(user_id)
        if user == None:
            return cls(user_id)
        return user