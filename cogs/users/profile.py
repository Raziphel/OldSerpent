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

        #! Quest 1 Complete
        # await self.bot.get_cog('Quests').get_quest(user=user, quest_no=1, completed=True)

        await self.base_profile(ctx=ctx, user=user, msg=None)



    async def base_profile(self, ctx, user, msg):
        if msg == None:
            msg = await ctx.send(embed=utils.ProfileEmbed(type="Default", user=user))
        else:
            await msg.edit(embed=utils.ProfileEmbed(type="Default", user=user))

        await msg.clear_reactions()
        #! adds the reactions
        # await msg.add_reaction("✨")
        await msg.add_reaction("💸")
        await msg.add_reaction("⛏")
        # await msg.add_reaction("❤️")
        # await msg.add_reaction("🏹")
        # await msg.add_reaction("🔮")

        # Watches for the reactions
        check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and x.emoji in ["💸", "⛏"]
        r, _ = await self.bot.wait_for('reaction_add', check=check)
        if r.emoji == "💸":
            await msg.edit(embed=utils.ProfileEmbed(type="Currency", user=user))
            pass
        if r.emoji == "⛏":
            await msg.edit(embed=utils.ProfileEmbed(type="Miners", user=user))
            pass
        await msg.clear_reactions()
        await msg.add_reaction("🔷")
        check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and x.emoji in ["🔷"]
        r, _ = await self.bot.wait_for('reaction_add', check=check)
        if r.emoji == "🔷":
            await self.base_profile(ctx=ctx, user=user, msg=msg)
            return




    @cooldown(1, 30, BucketType.user)
    @command(aliases=['c', 'C', 'Gems', 'ingots', 'gems', 'Ingots'])
    async def currency(self, ctx, user:Member=None):
        '''Quick Check Gems'''
        if not user:
            user = ctx.author
        m = await ctx.send(embed=utils.ProfileEmbed(type="Currency", user=user, quick=True), delete_after=15)




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
