import random
from datetime import datetime as dt
from utils.database import DatabaseConnection

class EmptySonas():
    def __init__(self):
        self.user_id = None
        self.verified = False
        self.name = "No name given"
        self.age = 18
        self.gender = "No gender given"
        self.sexuality = "No sexuality given"
        self.bio = "No bio given"
        self.image = None
        self.species = "No species given"
        self.color = 0
        self.likes = "No likes given"


class Nsfw_sonas(object):
    
    
    all_nsfw_sonas = {}
    empty = EmptySonas()

    def __init__(self, user_id:int, verified:bool, name:str, age:int, gender:str, sexuality:str, bio:str, image:str, species:str, color:int, likes:str):
        self.user_id = user_id
        self.verified = verified
        self.name = name
        self.age = age
        self.gender = gender
        self.sexuality = sexuality
        self.bio = bio
        self.image = image
        self.species = species
        self.color = color
        self.likes = likes

        self.all_nsfw_sonas[self.user_id] = self


    async def save(self, db:DatabaseConnection):
        '''
        Saves all of the connected user varibles
        '''
        try:
            await db('''
                INSERT INTO nsfw_sonas
                (user_id, verified, name, age, gender, sexuality, bio, image, species, color, likes)
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ''',
                self.user_id, self.verified, self.name, self.age, self.gender, self.sexuality, self.bio, self.image, self.species, self.color, self.likes
            )
        except Exception:
            await db('''
                UPDATE nsfw_sonas SET
                verified=$2, name=$3, age=$4, gender=$5, sexuality=$6, bio=$7, image=$8, species=$9, color=$10, likes=$11
                WHERE
                user_id=$1
                ''',
                self.user_id, self.verified, self.name, self.age, self.gender, self.sexuality, self.bio, self.image, self.species, self.color, self.likes
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets a user's connected varibles and sets defaults if there is none'''
        sona = cls.all_nsfw_sonas.get(user_id)
        if sona == None:
            return cls(
                user_id = user_id,
                verified = False,
                name = "No name given",
                age = 18,
                gender = "No gender given",
                sexuality = "No sexuality given",
                bio = "No bio given",
                image = None,
                species = "No species given",
                color = 0,
                likes = "No likes given",
            )
        return sona

    @classmethod
    def delete(cls, user_id:int):
        '''Removes a user from cache via their ID, fails silently if not present'''

        try:
            del cls.all_nsfw_sonas[user_id]
        except KeyError:
            pass

