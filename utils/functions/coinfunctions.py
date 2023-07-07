# Discord
from discord.ext.commands import command, cooldown, BucketType, Cog
from discord import Member, Message, User, TextChannel
# Utils
import utils


class CoinFunctions(object):
    bot = None

    @property
    async def tax_rate():
        return 0.08 

    @classmethod
    async def pay_user(cls, payer:Member, receiver:Member, amount:int):
        '''Use for payment between users (Taxed)'''

        #! Define Varibles
        cp = utils.Currency.get(payer.id)
        cr = utils.Currency.get(receiver.id)
        new_amount = await cls.pay_tax(payer=payer, amount=amount)
        taxed = amount - new_amount

        if cp.coins >= amount+taxed: #! Check they have enough coins to pay.
            cp.coins -= amount+taxed
            cr.coins += amount

        async with cls.bot.database() as db:
            await cp.save(db)
            await cr.save(db)
        return amount-new_amount #? Returns the amount taxed


    @classmethod 
    async def pay_tax(cls, payer:Member, amount:int):
        '''Use this method to pay the taxes for an amount then send the new amount back.'''

        #! Define Varibles
        cp = utils.Currency.get(payer.id)
        cr = utils.Currency.get(550474149332516881)

        #! Determine tax amount
        new_amount = amount*(1.00-cls.tax_rate) 
        taxed = amount - new_amount

        cp.coins -= taxed
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
        cr = utils.Currency.get(550474149332516881)

        cp.coins -= amount
        cr.coins += amount

        async with cls.bot.database() as db:
            await cp.save(db)
            await cr.save(db)

            
    @classmethod 
    async def earn(cls, earner:Member, amount:int):
        '''Use this method for letting users earn coins'''

        #! Define Varibles
        cu = utils.Currency.get(earner.id)
        cb = utils.Currency.get(550474149332516881)

        #! Check if the bank's got coins!
        if cb.coins <= 10000:
            
            return

        #! Just take it away from the bot!
        cu.coins += amount
        cb.coins -= amount

        async with cls.bot.database() as db:
            await cu.save(db)
            await cb.save(db)
