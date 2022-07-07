from utils.database import DatabaseConnection
import asyncpg

class Staff_Track(object):
    all_staff_track = {}

    def __init__(self, user_id:int, mutes:int=0, memes:int=0, nsfws:int=0, purges:int=0, messages:int=0, messages_month:int=0, mail_verification:int=0, mail_sonas:int=0):
        self.user_id = user_id
        self.mutes = mutes
        self.memes = memes
        self.nsfws = nsfws
        self.purges = purges
        self.messages = messages
        self.messages_month = messages_month
        self.mail_verification = mail_verification
        self.mail_sonas = mail_sonas

        self.all_staff_track[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO staff_track
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ''',
                self.user_id, self.mutes, self.memes, self.nsfws, self.mail_verification, self.messages, self.messages_month, self.purges, self.mail_sonas
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE staff_track SET
                mutes=$2, memes=$3, nsfws=$4, purges=$5, messages=$6, messages_month=$7, mail_verification=$8, mail_sonas=$9
                WHERE
                user_id=$1
                ''',
                self.user_id, self.mutes, self.memes, self.nsfws, self.purges, self.messages_month, self.messages, self.mail_verification, self.mail_sonas
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_staff_track.get(user_id)
        if user == None:
            return cls(user_id)
        return user
