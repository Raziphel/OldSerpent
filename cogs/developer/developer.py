
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

from asyncio import iscoroutine, gather
from traceback import format_exc

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
        for user in guild.members:
            await user.add_roles(mc, reason="opt-in!")
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
        bots = utils.DiscordGet(ctx.guild.roles, id=689618590638669845)
        everyone = utils.DiscordGet(ctx.guild.roles, id=689534383878701223)

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(muted, read_messages=None, send_messages=False, add_reactions=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False)
            await channel.set_permissions(bots, read_messages=True, send_messages=True, add_reactions=True, send_messages_in_threads=True, create_public_threads=True, create_private_threads=True)


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
        adult = utils.DiscordGet(guild.roles, id=1093881864806223932)
        adult2 = utils.DiscordGet(guild.roles, id=1141807070581112944)
        quirky = utils.DiscordGet(guild.roles, id=1129464175396143104)
        for user in guild.members:
            if (adult in user.roles) and (quirky in user.roles):
                mod = utils.Moderation.get(user.id)
                mod.adult = True
                mod.child = False
                await user.add_roles(adult2, reason="Reeee")
                await user.remove_roles(adult, reason="Reeee")
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
                lvl = utils.Levels.get(user.id)
                if lvl.level > 9:
                    c.coins += 25000
                    total += 25000
                async with self.bot.database() as db:
                    await c.save(db)
            except Exception as e:
                print(e) 

        await ctx.send(f"Handed out over **{total:,}x** {coin_e}!  To everyone level 10 or higher on the server!")



    @utils.is_dev()
    @command()
    async def fixseperators(self, ctx):
        '''Gives everyone seperator roles'''
        guild = self.bot.get_guild(self.bot.config['garden_id'])

        for user in guild.members:
            try:
                s1 = utils.DiscordGet(guild.roles, id=self.bot.config['seperator_roles']['access'])
                s2 = utils.DiscordGet(guild.roles, id=self.bot.config['seperator_roles']['purchases'])
                s3 = utils.DiscordGet(guild.roles, id=self.bot.config['seperator_roles']['pings'])
                s4 = utils.DiscordGet(guild.roles, id=self.bot.config['seperator_roles']['bio'])
                await user.add_roles(s1, reason="fixed")
                await user.add_roles(s2, reason="fixed")
                await user.add_roles(s3, reason="fixed")
                await user.add_roles(s4, reason="fixed")
                await sleep(1)
            except Exception as e:
                print(e) 

        await ctx.send(f"Fixed all the seperator roles!")


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
        async with self.bot.database() as db:
            await db('UPDATE currency SET lot_tickets = 0 WHERE lot_tickets > 0')
            





def setup(bot):
    x = Developer(bot)
    bot.add_cog(x)