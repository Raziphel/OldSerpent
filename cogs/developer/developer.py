
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


    @property  #! The currency logs
    def currency_log(self):
        return self.bot.get_channel(self.bot.config['channels']['currency_log'])

    @utils.is_dev()
    @command(aliases=['r'], hidden=True)
    async def restart(self, ctx):
        '''Restarts the bot'''  
        msg = await ctx.send(embed=utils.DevEmbed(title=f"Restarting..."))
        for num in range(3):
            await sleep(1)
            await msg.edit(embed=utils.DevEmbed(title=f"Restarting in {3-num}.", ))
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
        await message.edit(embed=utils.DevEmbed(desc=f"Ping:`{int(ping)}ms`\nUsers: `{users}`\nServers: `{servers}`"))


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
    @command()
    async def payday(self, ctx):
        '''Gives everyone some emeralds and diamonds as a payday!'''
        guild = self.bot.get_guild(self.bot.config['razisrealm_id'])

        emerald_e = self.bot.config['emotes']['emerald']
        diamond_e = self.bot.config['emotes']['diamond']
        ruby_e = self.bot.config['emotes']['ruby']

        for user in guild.members:
            try:
                c = utils.Currency.get(user.id)
                lvl = utils.Levels.get(user.id)
                emerald =25*(lvl.level*0.25)
                diamond = 5*(lvl.level*0.25)
                ruby = 1*(lvl.level*0.25)
                c.emerald += emerald
                c.diamond += diamond
                c.ruby += ruby
                await self.currency_log.send(embed=utils.LogEmbed(title=f"{user.name} recieved a payday.", desc=f"They recieved: {emerald_e} : **{emerald}**\n{diamond_e} : **{diamond}**\n{ruby_e} : **{ruby}**"))
                async with self.bot.database() as db:
                    await c.save(db)
            except:
                pass


    @utils.is_dev()
    @command()
    async def roles(self, ctx):
        '''Shows the amount of rules on the server'''
        roles = 0
        for role in ctx.guild.roles:
            roles += 1
        await ctx.send(f'**There are {roles} roles on the server!**')

    @utils.is_dev()
    @command(hidden=True)
    async def setdiamonds(self, ctx, user:Member, diamond:int):
        if user == None:
            user = ctx.author
        c = utils.Currency.get(user.id)
        c.diamond = diamond
        async with self.bot.database() as db:
            await c.save(db)

    @utils.is_dev()
    @command(hidden=True)
    async def setemeralds(self, ctx, user:Member, emerald:int):
        if user == None:
            user = ctx.author
        c = utils.Currency.get(user.id)
        c.emerald = emerald
        async with self.bot.database() as db:
            await c.save(db)

    @utils.is_dev()
    @command(hidden=True)
    async def setvc(self, ctx, user:Member, vc:int):
        if user == None:
            user = ctx.author
        s = utils.Tracking.get(user.id)
        s.vc_mins = vc
        async with self.bot.database() as db:
            await s.save(db)

    @utils.is_dev()
    @command(hidden=True)
    async def setmessages(self, ctx, user:Member, messages:int):
        if user == None:
            user = ctx.author
        s = utils.Tracking.get(user.id)
        s.messages = messages
        async with self.bot.database() as db:
            await s.save(db)





def setup(bot):
    x = Developer(bot)
    bot.add_cog(x)