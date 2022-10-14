import random
from datetime import datetime as dt
from utils.database import DatabaseConnection

class EmptySonas():
    def __init__(self):
        self.user_id = None
        self.slot = 1
        self.verified = False
        self.name = "No name given"
        self.age = "No age given"
        self.gender = "No gender given"
        self.sexuality = "No sexuality given"
        self.bio = "No bio given"
        self.image = None
        self.species = "No species given"
        self.height = "No height given"
        self.weight = "No weight given"
        self.archive_id = None
        self.fursona_id = None
        self.nsfw = False


class Sonas(object):
    
    
    all_sonas = {}
    empty = EmptySonas()

    def __init__(self, user_id:int, slot:int, verified:bool, name:str, age:str, gender:str, sexuality:str, bio:str, image:str, species:str, height:str, weight:str, archive_id:int, fursona_id:int, nsfw:bool):
        self.user_id = user_id
        self.slot = slot
        self.verified = verified
        self.name = name
        self.age = age
        self.gender = gender
        self.sexuality = sexuality
        self.bio = bio
        self.image = image
        self.species = species
        self.height = height
        self.weight = weight
        self.archive_id = archive_id
        self.fursona_id = fursona_id
        self.nsfw = nsfw

        self.all_sonas[self.user_id, self.slot] = self


    async def save(self, db:DatabaseConnection):
        '''
        Saves all of the connected user varibles
        '''
        try:
            await db('''
                INSERT INTO sonas
                (user_id, slot, verified, name, age, gender, sexuality, bio, image, species, height, weight, archive_id, fursona_id, nsfw)
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
                ''',
                self.user_id, self.slot, self.verified, self.name, self.age, self.gender, self.sexuality, self.bio, self.image, self.species, self.height, self.weight, self.archive_id, self.fursona_id, self.nsfw
            )
        except Exception:
            await db('''
                UPDATE sonas SET
                slot=$2, verified=$3, name=$4, age=$5, gender=$6, sexuality=$7, bio=$8, image=$9, species=$10, height=$11, weight=$12, archive_id=$13, fursona_id=$14, nsfw=$15
                WHERE
                user_id=$1
                ''',
                self.user_id, self.slot, self.verified, self.name, self.age, self.gender, self.sexuality, self.bio, self.image, self.species, self.height, self.weight, self.archive_id, self.fursona_id, self.nsfw
            )

    @classmethod
    def get(cls, user_id:int):
        '''Gets a user's connected varibles and sets defaults if there is none'''
        sona = cls.all_sonas.get(user_id)
        if sona == None:
            return cls(
                user_id = user_id,
                slot = slot, #! AAAAAAAA
                verified = False,
                name = "No name given",
                age = "No age given",
                gender = "No gender given",
                sexuality = "No sexuality given",
                bio = "No bio given",
                image = None,
                species = "No species given",
                height = "No height given",
                weight = "No weight given",
                fursona_id = None,
                archive_id = None,
                nsfw = False,
            )
        return sona

    @classmethod
    def delete(cls, user_id:int, slot:int):
        '''Removes a user from cache via their ID, fails silently if not present'''

        try:
            del cls.all_sonas[user_id, slot]
        except KeyError:
            pass

