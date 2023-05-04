# Discord
from discord.ext.commands import command, Cog
from discord import Member, Message, User, TextChannel
from discord.ext.tasks import loop
# Additions
from random import randint, choice
from datetime import datetime as dt, timedelta
from more_itertools import unique_everseen
from re import search
from asyncio import sleep

import utils

class Quests(Cog):
    def __init__(self, bot):
        self.bot = bot


    async def get_quest(self, user:Member, quest_no:int, completed:bool=False):
        #! Define Varibles
        q = utils.Quests.get(user.id)
        c = utils.Currency.get(user.id)
        lvl = utils.Levels.get(user.id)
        ite = utils.Items.get(user.id)

        if quest_no == 1: #! Make sure its quest no 1.
            if q.q1 == False: #! Make sure they haven't done the quest before.
                if completed == False: #! Results for if its done or not.
                    await user.send(embed=utils.QuestEmbed(name="Get some Coins!", desc="Click on a random Coin reward!!", tip="They pop up on messages randomly!"))
                    return
                else:
                    q.q1 = True #! now the quest is done.
                    await utils.CoinFunctions.earn(earner=message.author, amount=1000)
                    async with self.bot.database() as db:
                        await q.save(db)
                    await user.send(embed=utils.QuestEmbed(complete=True, name="Get some Coins!", reward=f"You gained: **1,000 Coins**"))
                    #! Give them 2nd quest!
                    if q.q2 == False:
                        await self.get_quest(user=user, quest_no=2)
                    return

        if quest_no == 2:
            if q.q2 == False: 
                if completed == False: 
                    await user.send(embed=utils.QuestEmbed(name="Check Your Profile!", desc="Do the most used command and view your profile!", tip="The command is /profile"))
                    return
                else:
                    q.q2 = True 
                    await utils.CoinFunctions.earn(earner=message.author, amount=1000)
                    async with self.bot.database() as db:
                        await q.save(db)
                    await user.send(embed=utils.QuestEmbed(complete=True, name="Check Your Profile!", reward=f"You gained: **1,000 Coins**"))
                    #! Give them 3rd quest!
                    if q.q3 == False:
                        await self.get_quest(user=user, quest_no=3)
                    return


        if quest_no == 3:
            if q.q3 == False: 
                if completed == False: 
                    await user.send(embed=utils.QuestEmbed(name="Claim your Daily!", desc="Remember to do /daily everyday to reap the rewards!", tip="..."))
                    return
                else:
                    q.q3 = True 
                    ite.lot_tickets += 5
                    async with self.bot.database() as db:
                        await q.save(db)
                        await ite.save(db)
                    await user.send(embed=utils.QuestEmbed(complete=True, name="Claim your Daily!", reward=f"**You got 5 lottery tickets!**"))
                    #! Give them 4th quest!
                    if q.q4 == False:
                        await self.bot.get_cog('Quests').get_quest(user=user, quest_no=4)
                    return

        if quest_no == 4:
            if q.q4 == False: 
                if completed == False: 
                    await user.send(embed=utils.QuestEmbed(name="Catch a bunny", desc="Catch a bunny when someone who has bunny luck spawns ones!", tip="There just a rare thing that'll happen."))
                    return
                else:
                    q.q4 = True 
                    ite.rabbit_luck += 1
                    async with self.bot.database() as db:
                        await q.save(db)
                        await ite.save(db)
                    await user.send(embed=utils.QuestEmbed(complete=True, name="Catch a bunny", reward=f"Guess what now you have bunny luck and could spawn some. <3"))
                    return

        if quest_no == 5:
            if q.q5 == False: 
                if completed == False: 
                    await user.send(embed=utils.QuestEmbed(name="Steal Someone's Money!", desc="Steal some coins from a fellow member!", tip="/steal [User]"))
                    return
                else:
                    q.q5 = True 
                    ite.thief_gloves += 5
                    async with self.bot.database() as db:
                        await q.save(db)
                        await ite.save(db)
                    await user.send(embed=utils.QuestEmbed(complete=True, name="Steal Someone's Money!", reward=f"For stealing you've earned: **5 More Gloves!** (Now have: {ite.thief_gloves:,})"))
                    return

        if quest_no == 6:
            if q.q6 == False: 
                if completed == False: 
                    await user.send(embed=utils.QuestEmbed(name="Gambler!", desc="Buy some lottery tickets!", tip="GAMBLING IS WRONG!"))
                    return
                else:
                    q.q6 = True 
                    ite.lot_tickets += 10
                    async with self.bot.database() as db:
                        await q.save(db)
                        await ite.save(db)
                    await user.send(embed=utils.QuestEmbed(complete=True, name="Gambler!", reward=f"**You got 10 lottery tickets!**"))
                    return

def setup(bot):
    x = Quests(bot)
    bot.add_cog(x)
