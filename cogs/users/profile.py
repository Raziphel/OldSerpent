#* Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group
from discord import Member, Message, User, Game, User
#* Additions
from datetime import datetime as dt, timedelta
from asyncio import sleep
from math import floor
#* Utils
import utils

class Profile(Cog):
    def __init__(self, bot):
        self.bot = bot


    @cooldown(1, 60, BucketType.channel)
    @command(aliases=['p', 'P', 'Profile'])
    async def profile(self, ctx, user:Member=None):
        '''Shows a user's profile'''
        if not user:
            user = ctx.author

        await ctx.send(embed=utils.ProfileEmbed(user=user))





    @cooldown(1, 5, BucketType.user)
    @command(aliases=['color', 'Color', 'Setcolor', 'SetColor'])
    async def setcolor(self, ctx, colour):
        '''Sets your user color'''
        colour_value = utils.Colors.get(colour.lower()) 
        ss = utils.Settings.get(ctx.author.id)

        if colour_value == None:
            try:
                colour_value = int(colour.strip('#'), 16)
            except ValueError:
                await ctx.send(embed=utils.SpecialEmbed(title="Incorrect colour usage!", guild=ctx.guild), delete_after=15)
                return

        ss.color = colour_value
        async with self.bot.database() as db:
            await ss.save(db)
        
        await ctx.send(embed=utils.DefualtEmbed(title="Your color setting has been set!", guild=ctx.guild, user=ctx.author), delete_after=15)




def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
