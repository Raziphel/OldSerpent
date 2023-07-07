
#* Discord
from discord.ext.commands import command, Cog
from discord import Member, PermissionOverwrite, Permissions

#*Additions
from asyncio import sleep, iscoroutine
from time import monotonic
from datetime import datetime as dt, timedelta
from random import choice
import utils
import os
import sys
import subprocess


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)



class Developer(Cog):
    def __init__(self, bot):
        self.bot = bot





    @utils.is_dev()
    @command()
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
    @command(aliases=['cult'])
    async def cultist(self, ctx, user:Member):
        await utils.UserFunction.verify_user(user=user, type="cultist")
        await ctx.send(embed=utils.DevEmbed(desc=f"<:Pentagram:1093983216244891689>"))


    @utils.is_dev()
    @command()
    async def optin(self, ctx):
        guild = self.bot.get_guild(self.bot.config['garden_id'])
        mc = utils.DiscordGet(guild.roles, id=1054143874538426368)
        scp = utils.DiscordGet(guild.roles, id=1054142893872398346)
        for user in guild.members:
            await user.add_roles(mc, reason="opt-in!")
            await user.add_roles(scp, reason="opt-in!!")
        await ctx.send(embed=utils.DevEmbed(desc=f"<:Pentagram:1093983216244891689>"))



    @utils.is_dev()
    @command(aliases=['r'])
    async def restart(self, ctx):
        '''Restarts the bot'''  
        msg = await ctx.send(embed=utils.DevEmbed(title=f"Restarting...", guild=ctx.guild))
        for num in range(5):
            await sleep(1)
            await msg.edit(embed=utils.DevEmbed(title=f"Restarting in {5-num}.", guild=ctx.guild))
        await ctx.message.delete()
        await msg.delete()
        python = sys.executable
        os.execl(python, python, *sys.argv)


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
        t.last_nitro_reward = dt.utcnow() - timedelta(days=50)
        async with self.bot.database() as db:
            await t.save(db)


    @utils.is_dev()
    @command()
    async def fixroles(self, ctx):
        muted = utils.DiscordGet(ctx.guild.roles, id=1028881308006502400)
        everyone = utils.DiscordGet(ctx.guild.roles, id=689534383878701223)

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(muted, read_messages=None, send_messages=False, add_reactions=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False)


        for channel in ctx.guild.voice_channels:
            await channel.set_permissions(muted, read_messages=None, send_messages=False, add_reactions=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False, connect=False)


        await ctx.send('Fixed Muted role!')



    @utils.is_dev()
    @command()
    async def setsticky(self, ctx):
        sti = utils.Sticky.get(ctx.channel.id)
        msg = await ctx.send('Making Sticky!')
        sti.message_id = msg.id
        async with self.bot.database() as db:
            await sti.save(db)



    @utils.is_dev()
    @command()
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
    @command()
    async def setmsgs(self, ctx, user:Member, amount:int):
        if not user:
            user = ctx.author
        c = utils.Tracking.get(user.id)
        c.messages = amount
        async with self.bot.database() as db:
            await c.save(db)

    @utils.is_dev()
    @command()
    async def setdaily(self, ctx, user:Member, amount:int):
        if not user:
            user = ctx.author
        c = utils.Daily.get(user.id)
        c.daily = amount
        async with self.bot.database() as db:
            await c.save(db)

    @utils.is_dev()
    @command()
    async def setvc(self, ctx, user:Member, amount:int):
        if not user:
            user = ctx.author
        c = utils.Tracking.get(user.id)
        c.vc_mins = amount
        async with self.bot.database() as db:
            await c.save(db)

    @utils.is_dev()
    @command()
    async def setcoins(self, ctx, user:Member, amount:int):
        if not user:
            user = ctx.author
        c = utils.Currency.get(user.id)
        c.coins = amount
        async with self.bot.database() as db:
            await c.save(db)

    @utils.is_dev()
    @command()
    async def addcoins(self, ctx, user:Member, amount:int):
        if not user:
            user = ctx.author
        coin_e = self.bot.config['emotes']['coin']
        c = utils.Currency.get(user.id)
        c.coins += amount
        await ctx.send(f"{user.mention} has earned {amount:,} {coin_e} !!!")
        async with self.bot.database() as db:
            await c.save(db)

    @utils.is_dev()
    @command()
    async def setlevel(self, ctx, user:Member, amount:int):
        if not user:
            user = ctx.author
        lvl = utils.Levels.get(user.id)
        lvl.level = amount
        async with self.bot.database() as db:
            await lvl.save(db)


    @utils.is_dev()
    @command()
    async def remove(self, ctx, user):
        utils.Levels.delete(user)
        utils.Currency.delete(user)
        print(f'{user} has been removed from db')


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
    @command()
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
    @command()
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
    @command()
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


    @utils.is_dev()
    @command()
    async def resettix(self, ctx):
        guild = self.bot.get_guild(self.bot.config['garden_id'])
        for member in utils.Currency.all_currency:
            c = utils.Items.get(member.id)
            c.lot_tickets = 0
            async with self.bot.database() as db:
                await c.save(db)




def setup(bot):
    x = Developer(bot)
    bot.add_cog(x)