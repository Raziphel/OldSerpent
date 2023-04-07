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

class item_usage(Cog):

    def __init__(self, bot):
        self.bot = bot
        # self.restart_cooldown = dt.utcnow()




    @cooldown(1, 3600, BucketType.user)
    @command(aliases=['Steal', 'yoink', 'Yoink'])
    async def steal(self, ctx, user:Member=None):
        '''
        Use your gloves to steal!
        '''

        # if (self.restart_cooldown + timedelta(minutes=30)) >= dt.utcnow():
        #     tf = self.restart_cooldown + timedelta(minutes=30)
        #     t = dt(1, 1, 1) + (tf - dt.utcnow())
        #     await ctx.send(embed=utils.DefualtEmbed(title=f"Stealing is on cooldown for another 30 minutes!", description=f"this is due to a bot restart recently!\n\nYou can steal again in {t.minute} minutes!"), delete_after=5)
        #     return

        if not user:
            await ctx.send(embed=utils.DefualtEmbed(title=f"You didn't say who your stealing from?", desc=f"**Stealing Odds:**\nSteal 2,000\nSteal 3,000\nSteal 4,000\nSteal 1%\nSteal 2%\nLose 3,000\nLose 2%"))
            return

        if user.id == self.bot.user.id:
            await ctx.send(embed=utils.DefualtEmbed(title=f"You can't steal from the master of thiefs!"))

        #! Define Varibles
        chance = choice(['2,000', '3,000', '4,000' '1%', '2%', '-3,000', '-2%'])
        c = utils.Currency.get(ctx.author.id)
        uc = utils.Currency.get(user.id)
        item = utils.Items.get(ctx.author.id)

        if item.thief_gloves <= 0:
            await ctx.send(embed=utils.DefualtEmbed(title=f"You don't have any gloves!"))
            return

        item.thief_gloves -= 1
        coins_stole = None
        coins_lost = None

        if chance == '2,000':
            coins_stole = 2000
            if uc.coins < coins_stole:
                coins_stole = uc.coins
            else:
                uc.coins -= coins_stole
                c.coins += coins_stole

        elif chance == '3,000':
            coins_stole = 3000
            if uc.coins < coins_stole:
                coins_stole = uc.coins
            else:
                uc.coins -= coins_stole
                c.coins += coins_stole

        elif chance == '4,000':
            coins_stole = 1000
            if uc.coins < coins_stole:
                coins_stole = uc.coins
            else:
                uc.coins -= coins_stole
                c.coins += coins_stole

        elif chance == '1%':
            coins_stole = floor(uc.coins*0.01)
            uc.coins -= coins_stole
            c.coins += coins_stole


        elif chance == '2%':
            coins_stole = floor(uc.coins*0.02)
            uc.coins -= coins_stole
            c.coins += coins_stole


        elif chance == '-2%':
            coins_stole = floor(uc.coins*0.02)
            uc.coins -= coins_stole
            c.coins += coins_stole

        elif chance == '-3,000':
            coins_lost = 1000
            if c.coins < coins_lost:
                coins_lost = c.coins
            else:
                uc.coins += coins_lost
                c.coins -= coins_lost


        coin_logs = self.bot.get_channel(self.bot.config['channels']['coin_logs'])
        if coins_lost != None:
            await ctx.send(content=f"{user.mention}", embed=utils.DefualtEmbed(title=f"🧤 Coins Stolen 🧤", desc=f"**{ctx.author}** tried to steal coins from **{user}** but, they lost **{coins_lost:,}** coins to them instead..."))
            await coin_logs.send(f"**{ctx.author}** tried to steal coins from **{user}** but, they lost **{coins_lost:,}** coins to them instead...")
        else:
            await ctx.send(content=f"{user.mention}", embed=utils.DefualtEmbed(title=f"🧤 Coins Stolen 🧤", desc=f"**{ctx.author}** Stole coins from **{user}** and they gained **{coins_stole:,}** coins!"))
            await coin_logs.send(f"**{ctx.author}** Stole coins from **{user}** and they gained **{coins_stole:,}** coins!")

        

        #! Quest Complete
        #await self.bot.get_cog('Quests').get_quest(user=ctx.author, quest_no=5, completed=True)


        async with self.bot.database() as db:
            await item.save(db)
            await c.save(db)
            await uc.save(db)





    # @command(aliases=['se', 'party', 'event'])
    # async def start_event(self, ctx):
    #     '''Starts a random event'''
    #     channel_id = str(ctx.channel.id)
    #     item = utils.Items.get(ctx.author.id)

    #     #! Quest 6 Complete
    #     await self.bot.get_cog('Quests').get_quest(user=ctx.author, quest_no=6, completed=True)

    #     #! Check for Party Poppers
    #     if item.party_popper <= 0:
    #         #! Check if its Razi
    #         if ctx.author.id != 159516156728836097:
    #             await ctx.send(embed=utils.DefualtEmbed(title=f"You don't have any Party Poppers!"))
    #             item.party_popper += 1
    #             return


    #     await self.bot.get_cog('event_handler').create_event(user=ctx.author, channel_id=channel_id, channel=ctx.channel)





def setup(bot):
    x = item_usage(bot)
    bot.add_cog(x)