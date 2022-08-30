
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
        t = utils.Timers.get(self.bot.config['razisrealm_id'])
        t.last_nitro_reward = (dt.now()-timedelta(days=50))
        async with self.bot.database() as db:
            await t.save(db)

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




    @utils.is_dev()
    @command(hidden=True)
    async def adults(self, ctx):
        '''Runs code through Python'''
        guild = self.bot.get_guild(self.bot.config['razisrealm_id']) #? Guild
        adult = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nsfw_adult'])
        adult2 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['adult'])
        for user in guild.members:
            if (adult in user.roles) or (adult2 in user.roles):
                mod = utils.Moderation(user.id)
                mod.adult = True
                mod.child = False
                async with self.bot.database() as db:
                        await mod.save(db)



    @utils.is_dev()
    @command()
    async def payday(self, ctx):
        '''Gives everyone some coins as a payday!'''
        guild = self.bot.get_guild(self.bot.config['razisrealm_id'])

        for user in guild.members:
            c = utils.Currency.get(user.id)
            lvl = utils.Levels.get(user.id)
            goodcoins = (lvl.level*5)
            c.good_coins += goodcoins
            print('giving a padyday!')

            async with self.bot.database() as db:
                await c.save(db)





def setup(bot):
    x = Developer(bot)
    bot.add_cog(x)