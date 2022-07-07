import random
from datetime import datetime as dt
from utils.database import DatabaseConnection

import asyncpg

class Interactions(object):
    all_interactions = {}

    def __init__(self, user_id:int, upvotes_given:int, upvotes_received:int, pats_given:int, pats_received:int, hugs_given:int, hugs_received:int, kisses_given:int, kisses_received:int, licks_given:int, licks_received:int, boops_given:int, boops_received:int, bites_given:int, bites_received:int, stabs_given:int, stabs_received:int, flirts_given:int, flirts_received:int, premium:bool=False):
        self.user_id = user_id
        self.upvotes_given = upvotes_given
        self.upvotes_received = upvotes_received
        self.pats_given = pats_given
        self.pats_received = pats_received
        self.hugs_given = hugs_given
        self.hugs_received = hugs_received
        self.kisses_given = kisses_given
        self.kisses_received = kisses_received
        self.licks_given = licks_given
        self.licks_received = licks_received
        self.boops_given = boops_given
        self.boops_received = boops_received
        self.bites_given = bites_given
        self.bites_received = bites_received
        self.stabs_given = stabs_given
        self.stabs_received = stabs_received
        self.flirts_given = flirts_given
        self.flirts_received = flirts_received
        self.premium = premium

        self.all_interactions[self.user_id] = self

    async def save(self, db:DatabaseConnection):
        '''
        Saves all of the connected user varibles
        '''
        try:
            await db('''
                INSERT INTO interactions
                (user_id, upvotes_given, upvotes_received, pats_given, pats_received, hugs_given, hugs_received, kisses_given, kisses_received, licks_given, licks_received, boops_given, boops_received, bites_given, bites_received, stabs_given, stabs_received, flirts_given, flirts_received, premium)
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20)
                ''',
                self.user_id, self.upvotes_given, self.upvotes_received, self.pats_given, self.pats_received, self.hugs_given, self.hugs_received, self.kisses_given, self.kisses_received, self.licks_given, self.licks_received, self.boops_given, self.boops_received, self.bites_given, self.bites_received, self.stabs_given, self.stabs_received, self.flirts_given, self.flirts_received, self.premium
            )
        except asyncpg.exceptions.UniqueViolationError:
            await db('''
                UPDATE interactions SET
                upvotes_given=$2, upvotes_received=$3, pats_given=$4, pats_received=$5, hugs_given=$6, hugs_received=$7, kisses_given=$8, kisses_received=$9, licks_given=$10, licks_received=$11, boops_given=$12, boops_received=$13, bites_given=$14, bites_received=$15, stabs_given=$16, stabs_received=$17, flirts_given=$18, flirts_received=$19, premium=$20
                WHERE
                user_id=$1
                ''',
                self.user_id, self.upvotes_given, self.upvotes_received, self.pats_given, self.pats_received, self.hugs_given, self.hugs_received, self.kisses_given, self.kisses_received, self.licks_given, self.licks_received, self.boops_given, self.boops_received, self.bites_given, self.bites_received, self.stabs_given, self.stabs_received, self.flirts_given, self.flirts_received, self.premium
            )

    @classmethod
    def get(cls, user_id:int):
        '''
        Gets a user's connected varibles and sets defaults if there is none
        '''
        interaction = cls.all_interactions.get(user_id)
        if interaction == None:
            return cls(
                user_id = user_id,
                upvotes_given = 0,
                upvotes_received = 0,
                pats_given = 0,
                pats_received = 0,
                hugs_given = 0,
                hugs_received = 0,
                kisses_given = 0,
                kisses_received = 0,
                licks_given = 0,
                licks_received = 0,
                boops_given = 0,
                boops_received = 0,
                bites_given = 0,
                bites_received = 0,
                stabs_given = 0,
                stabs_received = 0,
                flirts_given = 0,
                flirts_received = 0,
                premium = False,
            )
        return interaction
