import random
from datetime import datetime as dt
from utils.database import DatabaseConnection


class Quests(object):
    all_quests = {}

    def __init__(self, user_id:int, q1:bool, q2:bool, q3:bool, q4:bool, q5:bool, q6:bool, q7:bool, q8:bool, q9:bool):
        self.user_id = user_id
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6
        self.q7 = q7
        self.q8 = q8
        self.q9 = q9

        self.all_quests[self.user_id] = self


    async def save(self, db:DatabaseConnection):
        '''
        Saves all of the connected user varibles
        '''
        try:
            await db('''
                INSERT INTO quests
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ''',
                self.user_id, self.q1, self.q2, self.q3, self.q4, self.q5, self.q6, self.q7, self.q8, self.q9
            )
        except Exception:
            await db('''
                UPDATE quests SET
                q1=$2, q2=$3, q3=$4, q4=$5, q5=$6, q6=$7, q7=$8, q8=$9, q9=$10
                WHERE
                user_id=$1
                ''',
                self.user_id, self.q1, self.q2, self.q3, self.q4, self.q5, self.q6, self.q7, self.q8, self.q9
            )

    @classmethod
    def get(cls, user_id:int):
        '''
        Gets a user's connected varibles and sets defaults if there is none
        '''
        quest = cls.all_quests.get(user_id)
        if quest == None:
            return cls(
                user_id = user_id,
                q1 = False,
                q2 = False,
                q3 = False,
                q4 = False,
                q5 = False,
                q6 = False,
                q7 = False,
                q8 = False,
                q9 = False,
            )
        return quest

