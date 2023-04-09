# Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group, RoleConverter
from discord import Member, Message, User, Game, Embed
from discord import Member, Message, User, TextChannel, Role, RawReactionActionEvent, Embed
# Additions
from datetime import datetime as dt, timedelta
from asyncio import iscoroutine, gather, sleep
from math import floor 
from random import choice, randint

import utils


class supporters(Cog):

    def __init__(self, bot):
        self.bot = bot


    @command(application_command_meta=ApplicationCommandMeta(), aliases=['Monthly', 'claim', "Claim"])
    async def monthly(self, ctx):
        '''Supporters monthly claim of rewards!'''

        #! Define some mother fuckign varibles.
        day = utils.Daily.get(ctx.author.id)
        c = utils.Currency.get(ctx.author.id)
        nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['nitro'])
        t1 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t1'])
        t2 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t2'])
        t3 = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['t3'])
        supporterroles = [nitro, t1, t2, t3]

        #? Lets check if they are a supporter...
        supporter = False
        for role in ctx.author.roles:
            if role in supporterroles:
                supporter = True
                break

        #? Fuck em if they ain't a supporter.
        if supporter == False:
            await ctx.send(f"**Only supporters can claim a monthly reward!**", delete_after=6)
            return

        #! Check if it's first daily
        if not day.monthly:
            day.monthly = (day.monthly - timedelta(days=30))

        #! Check if already claimed
        if (day.monthly + timedelta(days=30)) >= dt.utcnow():
            tf = day.monthly + timedelta(days=30)
            t = dt(1, 1, 1) + (tf - dt.utcnow())
            await ctx.interaction.response.send_message(f"**You can claim your monthly rewards in {t.hour} hours and {t.minute} minutes!**")
            return

        #+ Determine and give rewards!
        if nitro in ctx.author.roles:
            reward = 10000
        if t1 in ctx.author.roles:
            reward = 20000
        if t2 in ctx.author.roles:
            reward = 30000
        if t3 in ctx.author.roles:
            reward = 40000
        c.coins += Reward
        async with self.bot.database() as db:
            await c.save(db)

        coin_e = self.bot.config['emotes']['coin']

        await interaction.response.edit_message(
            embed=utils.SpecialEmbed(
                title=f"Monthly Reward Claim!",
                desc=f"**Thanks for being a supporter!**\n\nGranted: {reward:,} {coin_e}****"
            ))
        return






def setup(bot):
    x = supporters(bot)
    bot.add_cog(x)