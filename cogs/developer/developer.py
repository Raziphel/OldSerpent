
#* Discord
from discord.ext.commands import command, Cog
from discord import Member, Message, User, Game, Embed
#*Additions
from asyncio import sleep, wait, iscoroutine
from time import monotonic
from datetime import datetime as dt, timedelta

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
        await self.bot.close()


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
    @command()
    async def boostrewards(self, ctx):
        '''Give nitros rewards now'''
        t = utils.Timers.get(self.bot.config['garden_id'])
        t.last_nitro_reward = dt.now() - timedelta(days=50)
        async with self.bot.database() as db:
            await t.save(db)



    @utils.is_dev()
    @command(hidden=True)
    async def ev(self, ctx, *, content:str):
        '''
        Runs code through Python
        '''
        try:
            ans = eval(content, globals(), locals())
        except Exception:
            await ctx.send('```py\n' + format_exc() + '```')
            return
        if iscoroutine(ans):
            ans = await ans
        await ctx.send('```py\n' + str(ans) + '```')




    @utils.is_dev()
    @command(hidden=True)
    async def adults(self, ctx):
        '''Runs code through Python'''
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        adult = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nsfw_adult'])
        adult2 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult'])
        for user in guild.members:
            if (adult in user.roles) or (adult2 in user.roles):
                mod = utils.Moderation.get(user.id)
                mod.adult = True
                mod.child = False
                async with self.bot.database() as db:
                    await mod.save(db)
                print(f'fixed {user.name}\'s adult roles!')


    @utils.is_dev()
    @command(hidden=True)
    async def setcoins(self, ctx, user:Member, amount:int):
        if not user:
            user = ctx.author
        c = utils.Currency.get(user.id)
        c.coins = amount
        async with self.bot.database() as db:
            await c.save(db)


    @utils.is_dev()
    @command(hidden=True)
    async def setlevel(self, ctx, user:Member, amount:int):
        if not user:
            user = ctx.author
        lvl = utils.Levels.get(user.id)
        lvl.level = amount
        async with self.bot.database() as db:
            await lvl.save(db)


    @utils.is_dev()
    @command()
    async def payday(self, ctx):
        '''Gives everyone some coins as a payday!'''
        guild = self.bot.get_guild(self.bot.config['garden_id'])
        total = 0
        coin_e = self.bot.config['emotes']['coin']

        for user in guild.members:
            try:
                c = utils.Currency.get(user.id)
                c.coins += 10000
                total += 10000
                print(f'{user.name} got payed!')
            except Exception as e:
                print(e) 

        await ctx.send(f"Handed out over **{total}x** {coin_e}!  To everyone on the server!")
        async with self.bot.database() as db:
            await c.save(db)


    @utils.is_dev()
    @command(hidden=True)
    async def randcomizelevels(self, ctx):
        guild = self.bot.get_guild(self.bot.config['garden_id'])
        for user in guild.members:
            for role in user.roles:
                lvl = utils.Levels.get(user.id)
                random = choice([-2,-1,0,1,2,3])
                lvl.level = lvl.level + random
            async with self.bot.database() as db:
                await lvl.save(db)
            print(f'{user.name} level set to {lvl.level}')
            await utils.UserFunction.check_level(user=user)
        await ctx.send('Level slightly ranzomized.')


    @utils.is_dev()
    @command(hidden=True)
    async def resetlevels(self, ctx):
        guild = self.bot.get_guild(self.bot.config['garden_id'])
        for user in guild.members:
            for role in user.roles:
                lvl = utils.Levels.get(user.id)
                if role.name == "Janitor":
                    lvl.level = 5
                elif role.name == "D-Class":
                    lvl.level = 11
                elif role.name == "Scientist":
                    lvl.level = 16
                elif role.name == "Head-Researcher":
                    lvl.level = 16
                elif role.name == "Containment Specialist":
                    lvl.level = 21
                elif role.name == "Facility Manager":
                    lvl.level = 26
                elif role.name == "MTF Operative":
                    lvl.level = 31
                elif role.name == "Chaos Insurgency":
                    lvl.level = 36
                elif role.name == "Serpent's Hand":
                    lvl.level = 100
                else: pass
            async with self.bot.database() as db:
                await lvl.save(db)
            print(f'{user.name} level set to {lvl.level}')
            await utils.UserFunction.check_level(user=user)
        await ctx.send('Level Reset Complete.')


    @utils.is_dev()
    @command(hidden=True)
    async def resetcoins(self, ctx):
        guild = self.bot.get_guild(self.bot.config['garden_id'])
        for user in guild.members:
            for role in user.roles:
                c = utils.Currency.get(user.id)
                if role.name == "Civilian":
                    c.coins = 1000
                elif role.name == "D-Class":
                    c.coins = 3000
                elif role.name == "Scientists":
                    c.coins = 8000
                elif role.name == "Facility Guards":
                    c.coins = 15000
                elif role.name == "Containment Engineers":
                    c.coins = 25000
                elif role.name == "Facility Managers":
                    c.coins = 50000
                elif role.name == "Mobile Task Force":
                    c.coins = 60000
                elif role.name == "Chaos Insurgency":
                    c.coins = 100000
                elif role.name == "Serpent's Hand":
                    c.coins = 500000
                else: pass
            async with self.bot.database() as db:
                await c.save(db)
            print(f'{user.name} coins set to {c.coins}')
        await ctx.send('Coin Reset Complete.')






def setup(bot):
    x = Developer(bot)
    bot.add_cog(x)