# Discord
from discord.ext.commands import command, Cog, cooldown, BucketType
from discord import Member
# Additions
from random import choice, randint
from time import monotonic
from asyncio import sleep
from math import floor

# Utils
import utils


class TooPoor(BaseException):
    pass


class Slots(Cog):
    def __init__(self, bot):
        self.bot = bot



    @cooldown(1, 10, BucketType.channel)
    @command(aliases=['Slots', 'slots', 'Slot', 'SlotMachine', 'slotmachine', 'playslots', 'playslot'])
    async def slot(self, ctx, amount:int=0):
        '''Take a chance in the slot machine.'''
        #? Check if bot is connected!
        if self.bot.connected == False:
            return


        c = utils.Currency.get(ctx.author.id)
        # items = utils.Items.get(ctx.author.id)
        msg = None

        #* Emojis
        silver_e = "<:Silver:994737895707525181>"
        gold_e = "<:Gold:994737893014773790>"
        emerald_e = "<:Emerald:994737891735511050>"
        diamond_e = "<:Diamond:994737890582069278>"
        ruby_e = "<:Ruby:994737896567357461>"
        sapphire_e = "<:Sapphire:994737897871782031>"
        amethyst_e = "<:Amethyst:994738216022319124> "
        crimson_e = "<:Crimson:994737894499569746>"

        if amount >= 5 and amount <= 100:
            pass 
        else:
            await ctx.send(f"You must enter a number higher than 5 and less than 100.", delete_after=15)
            return


        msg = await ctx.send(embed=utils.SpecialEmbed(title=f"[🌜] Slot Machine 🐍 [🌛]", desc=f"**Rewards:** [{gold_e} = {diamond_e}] [{ruby_e} = {sapphire_e}]\n🍀 1.25x Reward!\n✨ Common Reward!\n🍒 Uncommon Reward!\n🎀 Rare Reward!\n🦄 Epic Reward!\n\n__**Please pick the currency!**__", guild=ctx.guild, footer=" "))

        #! adds the reactions
        await msg.add_reaction(gold_e)
        await msg.add_reaction(ruby_e)

        try:
            #! Watches for the reactions
            check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and str(x.emoji) in [gold_e, ruby_e]
            r, _ = await self.bot.wait_for('reaction_add', check=check)

            await utils.GemFunction.pay_exchange(user=ctx.author)

            if str(r.emoji) == gold_e:
                currency = 'gold'
                emoji = gold_e
                reward_emoji = diamond_e
                if c.gold < amount:
                    raise TooPoor
            if str(r.emoji) == ruby_e:
                currency = 'ruby'
                emoji = ruby_e
                reward_emoji = sapphire_e
                if c.ruby < amount:
                    raise TooPoor

            await msg.clear_reactions()

        except TooPoor:
            await ctx.send(f'{ctx.author.mention} Payment denied. You would go in debt stupid!!!')
            return

        #! Define the rolls at pure chance! (These are open to change, but always for display.)
        slotsx = ['🍀', '✨', '🍒', '🎀', '🦄']
        slotsy = ['🍀', '✨', '🍒', '🎀', '🦄']
        slotsz = ['🍀', '✨', '🍒', '🎀', '🦄']
        x = choice(slotsx)
        slotsx.remove(x)
        y = choice(slotsy)
        slotsy.remove(x)
        z = choice(slotsz)
        slotsz.remove(z)

        rng = randint(1, 100)
        if rng < 5:
            slotsx = slotsy
        elif rng < 10:
            slotsy = slotsz

        if msg == None:
            msg = await ctx.send(embed=utils.SpecialEmbed(title=f"[🌜] Slot Machine 🐍 [🌛]", desc=f"The slot machine is now rolling... [4]", guild=ctx.guild, footer=" "))
        else:
            await msg.edit(embed=utils.SpecialEmbed(title=f"[🌜] Slot Machine 🐍 [🌛]", desc=f"The slot machine is now rolling... [4]", guild=ctx.guild, footer=" "))

        for num in range(4):
            await msg.edit(embed=utils.SpecialEmbed(title=f"[🌜] Slot Machine 🐍 [🌛]", desc=f"[{choice(slotsx)}-{choice(slotsy)}-{choice(slotsz)}]\n[{choice(slotsx)}-{choice(slotsy)}-{choice(slotsz)}]\n[{choice(slotsx)}-{choice(slotsy)}-{choice(slotsz)}]\n\nThe slot machine is now rolling... [{4-num}]", guild=ctx.guild, footer=" "))
            await sleep(1)

        reward = None
        reward_amount = 0
        if x == "🍀" and y == "🍀" and z == "🍀":
            reward_amount = round(amount/5)

        if x == "✨" and y == "✨" and z == "✨":
            reward_amount = round(amount/4)

        if x == "🍒" and y == "🍒" and z == "🍒":
            reward_amount = round(amount/3)

        if x == "🎀" and y == "🎀" and z == "🎀":
            reward_amount = round(amount/2)

        if x == "🦄" and y == "🦄" and z == "🦄":
            reward_amount = round(amount/1)

        if reward_amount > 0:
            if currency == 'gold':
                c.diamond += reward_amount
            elif currency == 'ruby':
                c.sapphire += reward_amount
            reward = f"You recieved {reward_amount}x {reward_emoji}!"


        if reward == None:
            await msg.edit(embed=utils.SpecialEmbed(title=f"[🌜] Slot Machine 🦄 [🌛]", desc=f"`[{choice(slotsx)}-{choice(slotsy)}-{choice(slotsz)}]`\n-[{x}-{y}-{z}]-\n`[{choice(slotsx)}-{choice(slotsy)}-{choice(slotsz)}]`\n\nYou have lost `{amount}` {currency} {emoji}.", guild=ctx.guild, footer=" "))
            if currency == 'silver':
                c.silver -= reward_amount
            elif currency == 'gold':
                c.gold -= reward_amount
            elif currency == 'emerald':
                c.emerald -= reward_amount
            elif currency == 'diamond':
                c.diamond -= reward_amount

        else:
            await msg.edit(embed=utils.SpecialEmbed(title=f"[🌜] Slot Machine 🦄 [🌛]", desc=f"`[{choice(slotsx)}-{choice(slotsy)}-{choice(slotsz)}]`\n-[{x}-{y}-{z}]-\n`[{choice(slotsx)}-{choice(slotsy)}-{choice(slotsz)}]`\n\n**{reward}**", guild=ctx.guild, footer=" "))

        await utils.GemFunction.update_gems(user=ctx.author)





def setup(bot):
    x = Slots(bot)
    bot.add_cog(x)