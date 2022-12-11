# Discord
from discord.ext.commands import command, cooldown, BucketType, Cog
from discord import Member, Message, User
# Utils
import utils

class Payment(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  #! The members logs
    def server_log(self):
        return self.bot.get_channel(self.bot.config['channels']['server']) #?Coins log channel

    @cooldown(1, 360, BucketType.channel)
    @command(aliases=['send'])
    async def pay(self, ctx, receiver:User=None, amount:int=0):
        '''sending payemnts to other members'''
        if not receiver:
            await ctx.send(embed=utils.DefualtEmbed(desc=f"{ctx.author} `->pay (user) (amount)`"))
            return
        if receiver == ctx.author:
            await ctx.send(embed=utils.DefualtEmbed(desc=f"{ctx.author} You can't pay yourself coins! stupid..."))
            return
        if amount <= 10:
            await ctx.send(embed=utils.DefualtEmbed(desc=f"{ctx.author} Has to be more than 10!"))
            return
        c = utils.Currency.get(ctx.author.id)
        if amount > c.coins:
            await ctx.send(embed=utils.DefualtEmbed(desc=f"{receiver.mention} you don't have that many coins."))
            return

        await utils.CoinFunctions.pay_user(payer=ctx.author, receiver=receiver, amount=amount)

        await ctx.send(embed=utils.DefualtEmbed(desc=f"**{ctx.author} sent {amount} coins to {receiver}!**"))

        await self.server_log.send(embed=utils.LogEmbed(type="special", desc=f"{ctx.author} payed {amount} coins to {receiver}!"))







def setup(bot):
    x = Payment(bot)
    bot.add_cog(x)