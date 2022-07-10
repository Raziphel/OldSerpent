
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

    @utils.is_dev()
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


    @utils.is_dev()
    @command(hidden=True)
    async def resetlevels(self, ctx):
        guild = self.bot.get_guild(self.bot.config['razisrealm_id'])
        for user in guild.members:
            for role in user.roles:
                lvl = utils.Levels.get(user.id)
                if role.name == "Pawn [1~5]":
                    lvl.level = 5
                elif role.name == "Knight [6~15]":
                    lvl.level = 15
                elif role.name == "Knight Rook [16~25]":
                    lvl.level = 25
                elif role.name == "Bishop [26~40]":
                    lvl.level = 40
                elif role.name == "Queen [41~60]":
                    lvl.level = 60
                elif role.name == "King [61~80]":
                    lvl.level = 80
                elif role.name == "Challenger [51-90]":
                    lvl.level = 90
                elif role.name == "Master [91-99]":
                    lvl.level = 99
                elif role.name == "Grand Master [100]":
                    lvl.level = 100
                else: pass
            async with self.bot.database() as db:
                await lvl.save(db)
            print(f'{user.name} level set to {lvl.level}')
        await ctx.send('Level Reset Complete.')


def setup(bot):
    x = Developer(bot)
    bot.add_cog(x)