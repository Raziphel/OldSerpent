# Discord
from discord.ext.commands import command, Cog, cooldown, BucketType
from discord import Member
# Additions
from random import choice, randint
from time import monotonic
from asyncio import sleep

# Utils
import utils

class Interactions(Cog):
    def __init__(self, bot):
        self.bot = bot


    @cooldown(1, 120, BucketType.user)
    @command(aliases=['patpat', 'Pat', 'pats'])
    async def pat(self, ctx, user:Member):
        '''gives a pat!'''

        giver_int = utils.Interactions.get(ctx.author.id)
        receiver_int = utils.Interactions.get(user.id)
        author = ctx.author
        if author.id == user.id:
            msg = await ctx.send(f"No, patting yourself weirdo...", delete_after=15)
            return

        msg = choice([
            f"*{author.mention} felt like {user.mention} was on their best behavior and rewarded them by ruffling their hair.*",
            f"*{author.mention} places their hand on top of {user.mention}'s head and ruffles their hair, aww!*",
            f"*{user.mention} just got rewarded with some headpats by {author.mention}, that's sweet of them!*",
            f"*Gasp! {user.mention}'s hair is a mess due to the pats {author.mention} gave them.*",
            f"*{author.mention} gently headpats {user.mention}, ruffling their hair.*", 
        ])

        giver_int.pats_given += 1
        receiver_int.pats_received += 1
        async with self.bot.database() as db:
            await giver_int.save(db)
            await receiver_int.save(db)

        await ctx.send(msg)


    @cooldown(1, 120, BucketType.user)
    @command(aliases=['Hug', 'hugs', 'Hugs'])
    async def hug(self, ctx, user: Member):
        '''gives a hug!'''

        giver_int = utils.Interactions.get(ctx.author.id)
        receiver_int = utils.Interactions.get(user.id)
        author = ctx.author

        if ctx.author.id == user.id:
            msg = await ctx.send(f"You can not hug yourself, sad honestly...", delete_after=15)
            return

        msg = choice([
            f"*{author.mention} tightly wraps their arms around {user.mention} for a hug*",
            f"*{author.mention} tackles {user.mention} to the ground, hugging them as tight as possible *",
            f"*{author.mention} notices {user.mention} is shivering from the cold, and decides to give them a hug to warm them up!*",
            f"*{author.mention} made the decision to grab {user.mention} by the arm, pull them in and hug them as tight as they could!*",
            
        ])

        giver_int.hugs_given += 1
        receiver_int.hugs_received += 1
        async with self.bot.database() as db:
            await giver_int.save(db)
            await receiver_int.save(db)

        await ctx.send(msg)

    @utils.is_nsfw()
    @cooldown(1, 120, BucketType.user)
    @command(aliases=['Kiss', 'kisses', 'Kisses', 'kissy', 'Kissy', 'smooch'])
    async def kiss(self, ctx, user: Member):
        '''gives a kiss!'''
        giver_int = utils.Interactions.get(ctx.author.id)
        receiver_int = utils.Interactions.get(user.id)
        adult = False
        author = ctx.author

        if ctx.author.id == user.id:
            msg = await ctx.send(f"Kissing yourself? In public?", delete_after=15)
            return


        msg = choice([
            f"*{author.mention} gently presses their lips against {user.mention} for a soft kiss*",
            f"*{author.mention} turns {user.mention}'s head a little bit to the side before planting a kiss on their cheek, isn't that cute!*",
            f"*{author.mention} leans up and plants a kiss on {user.mention}'s forehead, how generous.*",
            f"*{author.mention} rubs their nose up against {user.mention}'s nose for a cute eskimokiss.*",
        ])

        giver_int.kisses_given += 1
        receiver_int.kisses_received += 1
        async with self.bot.database() as db:
            await giver_int.save(db)
            await receiver_int.save(db)

        await ctx.send(msg)

    @utils.is_nsfw()
    @cooldown(1, 120, BucketType.user)
    @command(aliases=['Lick', 'licks', 'Licks', 'lix', 'Lix'])
    async def lick(self, ctx, user: Member):
        '''gives a lick!'''
        giver_int = utils.Interactions.get(ctx.author.id)
        receiver_int = utils.Interactions.get(user.id)
        adult = False
        author = ctx.author

        if ctx.author.id == user.id:
            msg = await ctx.send(f"Thats weird... :c", delete_after=15)
            return


        msg = choice([
            f"*Oh my, {author.mention} drags their tongue against {user.mention}'s cheek.*",
            f"*{author.mention} sticks out their tongue at {user.mention}, licking their nose, that's gay!*",
        ])

        giver_int.licks_given += 1
        receiver_int.licks_received += 1
        async with self.bot.database() as db:
            await giver_int.save(db)
            await receiver_int.save(db)

        await ctx.send(msg)


    @cooldown(1, 120, BucketType.user)
    @command(aliases=['Boop', 'boops'])
    async def boop(self, ctx, user: Member):
        '''gives a boop!'''
        giver_int = utils.Interactions.get(ctx.author.id)
        receiver_int = utils.Interactions.get(user.id)
        author = ctx.author

        if giver_int.premium == False:
            msg = await ctx.send(f"Sorry that is a premium interaction!", delete_after=15)
            return

        if ctx.author.id == user.id:
            msg = await ctx.send(f"{author.mention} boops him self???", delete_after=15)
            return

        msg = choice([
            f"*{author.mention} presses their finger against {user.mention}'s nose. Boop!*",
            f"*{user.mention} looks at their nose as they suddenly feel {author.mention} booping them.*",
            f"*{user.mention} sneezes when they're suddenly booped by {author.mention}*",
            f"*{author.mention} gave a lil boop to the snoot to {user.mention}!*",
        ])

        giver_int.boops_given += 1
        receiver_int.boops_received += 1
        async with self.bot.database() as db:
            await giver_int.save(db)
            await receiver_int.save(db)

        await ctx.send(msg)


    @utils.is_nsfw()
    @cooldown(1, 120, BucketType.user)
    @command(aliases=['Bite', 'bites'])
    async def bite(self, ctx, user: Member):
        '''gives a bite!'''
        giver_int = utils.Interactions.get(ctx.author.id)
        receiver_int = utils.Interactions.get(user.id)
        author = ctx.author

        if ctx.author.id == user.id:
            msg = await ctx.send(f"{author.mention} tried biting himself make fun of the sub.", delete_after=15)
            return

        if giver_int.premium == False:
            msg = await ctx.send(f"Sorry that is a premium interaction!", delete_after=15)
            return


        msg = choice([
            f"*{author.mention} wants to annoy {user.mention}, and decides to do so by gently nibbling on their arm.*",
            f"*{user.mention} blushes slightly as {author.mention} softly bites the crook of their neck.*",
            f"*{author.mention} leans foward and playfully bites into {user.mention}'s nose.*",
        ])

        giver_int.bites_given += 1
        receiver_int.bites_received += 1
        async with self.bot.database() as db:
            await giver_int.save(db)
            await receiver_int.save(db)

        await ctx.send(msg)


    @cooldown(1, 120, BucketType.user)
    @command(aliases=['Stab', 'stabs', 'kill'])
    async def stab(self, ctx, user: Member):
        '''gives a stab!'''
        giver_int = utils.Interactions.get(ctx.author.id)
        receiver_int = utils.Interactions.get(user.id)
        author = ctx.author

        if giver_int.premium == False:
            msg = await ctx.send(f"Sorry that is a premium interaction!", delete_after=15)
            return

        if ctx.author.id == user.id:
            msg = await ctx.send(f"I can't enourage self harm.", delete_after=15)
            return

        msg = choice([
            f"*{author.mention} is tired of {user.mention}'s shit, and decides to stab them in the side. How to get away with murder, huh?*",
            f"*While cooking, {author.mention} accidentally trips and falls over, stabbing themselves and bled out on the floor. Uh oh!*",
        ])

        giver_int.stabs_given += 1
        receiver_int.stabs_received += 1
        async with self.bot.database() as db:
            await giver_int.save(db)
            await receiver_int.save(db)

        await ctx.send(msg)

    @utils.is_nsfw()
    @cooldown(1, 120, BucketType.user)
    @command(aliases=['Flirt', 'flirts'])
    async def flirt(self, ctx, user: Member):
        '''gives a flirt!'''
        giver_int = utils.Interactions.get(ctx.author.id)
        receiver_int = utils.Interactions.get(user.id)
        author = ctx.author

        if ctx.author.id == user.id:
            msg = await ctx.send(f"Thats so sad...", delete_after=15)
            return

        if giver_int.premium == False:
            msg = await ctx.send(f"Sorry that is a premium interaction!", delete_after=15)
            return

        if ctx.channel.is_nsfw() == False:
            msg = await ctx.send(f"Sorry that command can only be run in NSFW channels.", delete_after=15)
            return

        msg = choice([
            f"*{author.mention} buys {user.mention} a drink and asks if they come here often*",
            f"*{user.mention} opens their front door, seeing a beautiful bouquet of roses with a small note from {author.mention}. That's adorable!*",
            f"*{author.mention} nervously walks up to {user.mention} and asks them if they would maybe like to get a cup of coffee sometime..?*",
        ])

        giver_int.flirts_given += 1
        receiver_int.flirts_received += 1
        async with self.bot.database() as db:
            await giver_int.save(db)
            await receiver_int.save(db)

        await ctx.send(msg)


def setup(bot):
    x = Interactions(bot)
    bot.add_cog(x)