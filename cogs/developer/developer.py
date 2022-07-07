
#* Discord
from discord.ext.commands import command, Cog
from discord import Member, Message, User, Game, Embed
#*Additions
from asyncio import sleep, wait, iscoroutine
from time import monotonic

import utils

class Developer(Cog):
    def __init__(self, bot):
        self.bot = bot


    @utils.is_dev()
    @command(aliases=['r'], hidden=True)
    async def restart(self, ctx):
        '''Restarts the bot'''  
        msg = await ctx.send(embed=utils.DevEmbed(title=f"Restarting...", guild=ctx.guild))
        for num in range(5):
            await sleep(1)
            await msg.edit(embed=utils.DevEmbed(title=f"Restarting in {5-num}.", guild=ctx.guild))
        await ctx.message.delete()
        await msg.delete()
        await self.bot.logout()


    @command()
    async def ping(self, ctx):
        '''Checks bot's ping'''
        await sleep(1)
        await ctx.message.delete()
        before = monotonic()
        message = await ctx.send("Pong!")
        ping = (monotonic() - before) * 1000
        users = len(set(self.bot.get_all_members()))
        servers = len(self.bot.guilds)
        await message.edit(embed=utils.DevEmbed(desc=f"Ping:`{int(ping)}ms`\nUsers: `{users}`\nServers: `{servers}`", guild=ctx.guild))


    @utils.is_dev()
    @command(hidden=True)
    async def ev(self, ctx, *, content:str):
        '''Runs code through Python'''
        try:
            ans = eval(content, globals(), locals())
        except Exception:
            await ctx.send('```py\n' + format_exc() + '```')
            return
        if iscoroutine(ans):
            ans = await ans
        await ctx.send('```py\n' + str(ans) + '```')


    @command(hidden=True)
    async def premium(self, ctx):
        inter = utils.Interactions.get(ctx.author.id)
        inter.premium = True
        async with self.bot.database() as db:
            await inter.save(db)
        await ctx.send(f"Premium Interactions allowed.")

    @utils.is_owner_staff()
    @command()
    async def roles(self, ctx):
        roles = 0
        for role in ctx.guild.roles:
            roles += 1
        await ctx.send(f'**There are {roles} roles on the server!**')


    @utils.is_dev()
    @command(hidden=True)
    async def setlvl(self, ctx, level:int):
        lvl = utils.Levels.get(ctx.author.id)
        lvl.level = level
        async with self.bot.database() as db:
            await lvl.save(db)




    @utils.is_dev()
    @command(hidden=True)
    async def setruby(self, ctx, amount:int):
        c = utils.Currency.get(ctx.author.id)
        c.ruby = amount
        async with self.bot.database() as db:
            await c.save(db)



def setup(bot):
    x = Developer(bot)
    bot.add_cog(x)