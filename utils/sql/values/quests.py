from utils.database import DatabaseConnection
import asyncpg

class Quests(object):
    all_quests = {}

    def __init__(self, user_id:int, main_quest:str="Choose Start", side_quest:str="Go Fishing"):
        self.user_id = user_id
        self.main_quest = main_quest
        self.side_quest = side_quest

        self.all_quests[self.user_id] = self


    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO quests
                VALUES
                ($1, $2, $3)
                ''',
                self.user_id, self.main_quest, self.side_quest
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE quests SET
                main_quest=$2, side_quest=$3
                WHERE
                user_id=$1
                ''',
                self.user_id, self.main_quest, self.side_quest
            )


    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_quests.get(user_id)
        if user == None:
            return cls(user_id)
        return user


