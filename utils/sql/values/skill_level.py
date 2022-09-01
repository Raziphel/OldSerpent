from utils.database import DatabaseConnection
from datetime import datetime as dt, timedelta
import asyncpg

class Skill_Level(object):
    all_levels = {}

    def __init__(self, user_id:int, combat:int=1, c_exp:int=0, mining:int=1, m_exp:int=0, herbalism:int=1, h_exp:int=0, woodcutting:int=1, w_exp:int=0, fishing:int=1, f_exp:int=0):
        self.user_id = user_id
        self.combat = combat
        self.c_exp = c_exp
        self.mining = mining
        self.m_exp = m_exp
        self.herbalism = herbalism
        self.h_exp = h_exp
        self.woodcutting = woodcutting
        self.w_exp = w_exp
        self.fishing = fishing
        self.f_exp = f_exp

        self.all_levels[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''Saves all of the connected user varibles'''
        try:
            await db('''
                INSERT INTO skill_level
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ''',
                self.user_id, self.combat, self.c_exp, self.mining, self.m_exp, self.herbalism, self.h_exp, self.woodcutting, self.w_exp, self.fishing, self.f_exp
            )
        except asyncpg.exceptions.UniqueViolationError: 
            await db('''
                UPDATE skill_level SET
                combat=$2, c_exp=$3 mining=$4, m_exp=$5, herbalism=$6, h_exp=$7, woodcutting=$8, w_exp=$9, fishing=$10, f_exp=$11
                WHERE
                user_id=$1
                ''',
                self.user_id, self.combat, self.c_exp, self.mining, self.m_exp, self.herbalism, self.h_exp, self.woodcutting, self.w_exp, self.fishing, self.f_exp,
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets level table's connected varibles'''
        user = cls.all_levels.get(user_id)
        if user == None:
            return cls(user_id)
        return user

    @classmethod
    def sort_combat(cls):
        '''sorts the user's by balance. getting ranks!'''
        sorted_combat = sorted(cls.all_levels.values(), key=lambda u: u.combat, reverse=True)
        return sorted_combat