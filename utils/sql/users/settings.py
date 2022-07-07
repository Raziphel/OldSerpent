import asyncpg

from utils.database import DatabaseConnection


class Settings(object):
    all_users_settings = {}

    def __init__(self, user_id:int, vc_msgs:bool=False, color:int=0xff69b4):
        self.user_id = user_id
        self.vc_msgs = vc_msgs
        self.color = color

        self.all_users_settings[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''

        try:
            await db('''
                INSERT INTO settings
                VALUES
                ($1, $2, $3)
                ''',
                self.user_id, self.vc_msgs, self.color
            )
        except asyncpg.exceptions.UniqueViolationError:
            await db('''
                UPDATE settings SET
                vc_msgs=$2, color=$3
                WHERE
                user_id=$1
                ''',
                self.user_id, self.vc_msgs, self.color
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets daily table's connected varibles'''

        user = cls.all_users_settings.get(user_id)
        if user is None:
            return cls(
                user_id=user_id,
                vc_msgs=0,
                color=0xff69b4,
            )
        return user
