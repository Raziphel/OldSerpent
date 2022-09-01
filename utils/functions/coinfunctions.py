# Discord
from discord.ext.commands import command, cooldown, BucketType, Cog
from discord import Member, Message, User, TextChannel
# Utils
import utils


class CoinFunctions(object):
    bot = None

    @classmethod
    async def pay_user(cls, payer:Member, receiver:Member, amount:int):
        '''Use for payment between users (Taxed)'''

        #! Define Varibles
        cp = utils.Currency.get(payer.id)
        cr = utils.Currency.get(receiver.id)
        amount = await cls.pay_tax(payer=payer, amount=amount)

        if cp.coins >= amount: #! Check they have enough coins to pay.
            cp.coins -= amount
            cr.coins += amount

        async with cls.bot.database() as db:
            await cp.save(db)
            await cr.save(db)


    @classmethod 
    async def pay_tax(cls, payer:Member, amount:int):
        '''Use this method to pay the taxes for an amount then send the new amount back.'''

        #! Define Varibles
        cp = utils.Currency.get(payer.id)
        cr = utils.Currency.get(cls.bot.user.id)

        #! Determine tax amount
        new_amount = amount*0.92 #? 8% Tax
        taxed = amount - new_amount

        cp.coins -= taxed
        cp.tax += taxed
        cr.coins += taxed

        async with cls.bot.database() as db:
            await cp.save(db)
            await cr.save(db)

        return new_amount


    @classmethod 
    async def pay_for(cls, payer:Member, amount:int):
        '''Use this method for purchases made!'''

        #! Define Varibles
        cp = utils.Currency.get(payer.id)
        cr = utils.Currency.get(cls.bot.user.id)

        cp.coins -= amount
        cr.coins += amount

        async with cls.bot.database() as db:
            await cp.save(db)
            await cr.save(db)