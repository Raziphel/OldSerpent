
#* Discord
from discord.ext.commands import command, Cog
from discord import Member, Message, User, Game, Embed
#*Additions
from asyncio import sleep, wait, iscoroutine
from time import monotonic
from datetime import datetime as dt, timedelta

from contextlib import redirect_stdout
from io import StringIO
from textwrap import indent
from traceback import format_exc

from aiohttp import ClientSession
from discord import User, File

import utils

class Developer(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None


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


    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""

        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            if content[-4] == '\n':
                return '\n'.join(content.split('\n')[1:-1])
            return '\n'.join(content.split('\n')[1:]).rstrip('`')

        # remove `foo`
        return content.strip('` \n')


    @utils.is_dev()
    @command(hidden=True)
    async def ev(self, ctx, *, content: str):
        '''
        Evaluates some Python code
        '''

        # Make the environment
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
            'self': self,
        }
        env.update(globals())

        # Make code and output string
        content = self.cleanup_code(content)
        stdout = StringIO()
        to_compile = f'async def func():\n{indent(content, "  ")}'

        # Make the function into existence
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        # Grab the function we just made and run it
        func = env['func']
        try:
            # Shove stdout into StringIO
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            # Oh no it caused an error
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{format_exc()}\n```')
        else:
            # Oh no it didn't cause an error
            value = stdout.getvalue()

            # Give reaction just to show that it ran
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            # If the function returned nothing
            if ret is None:
                # It might have printed something
                if value:
                    await ctx.send(f'```py\n{value}\n```')

            # If the function did return a value
            else:
                self._last_result = ret
                text = f'```py\n{value}{ret}\n```'
                if len(text) > 2000:
                    return await ctx.send(file=File(StringIO('\n'.join(text.split('\n')[1:-1])), filename='ev.txt'))
                await ctx.send(text)




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
        print('fix adult roles!')




    @utils.is_dev()
    @command()
    async def payday(self, ctx):
        '''Gives everyone some coins as a payday!'''
        guild = self.bot.get_guild(self.bot.config['razisrealm_id'])

        for user in guild.members:
            try:
                c = utils.Currency.get(user.id)
                c.coins += 1000
                print(f'{user.name} got payed!')
            except Exception as e:
                print(e) 

            async with self.bot.database() as db:
                await c.save(db)




def setup(bot):
    x = Developer(bot)
    bot.add_cog(x)