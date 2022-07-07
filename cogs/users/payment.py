# Discord
from discord.ext.commands import command, cooldown, BucketType, Cog
from discord import Message, User
# Utils
import utils


class TooPoor(BaseException):
    pass


class Payment(Cog):
    def __init__(self, bot):
        self.bot = bot



    @cooldown(1, 86400, BucketType.channel) #! So thats a day in seconds
    @command(aliases=['send'])
    async def pay(self, ctx, receiver:User=None, gems:int=0):
        '''
        sending payemnts to other members
        '''
        #? Check if bot is connected!
        if self.bot.connected == False:
            return


        if not receiver:
            await ctx.send(embed=utils.SpecialEmbed(description=f"{ctx.author.mention} `.pay (user) (amount)`", guild=ctx.guild))
            return

        c = utils.Currency.get(ctx.author.id)
        c_r = utils.Currency.get(receiver.id)

        #* Emojis
        amethyst_e = "<:Amethyst:766123218732843019>"
        diamond_e = "<:Diamond:766123219609976832>"
        emerald_e = "<:Emerald:766123219731611668>"
        phel_e = "<:crimson:766123219781419020>"
        silver_e = "<:Silver:766123219761233961>"
        gold_e = "<:GoldIngot:766123219827949596>"
        sapphire_e = "<:Sapphire:766123220201635850>"
        ruby_e = "<:Ruby:766123219928481852>"

        if receiver == ctx.author:
            await ctx.send(embed=utils.SpecialEmbed(description=f"{ctx.author.mention} You can't pay yourself gems! stupid...", guild=ctx.guild))
            return
        if gems <= 0 or gems > 100:
            await ctx.send(embed=utils.SpecialEmbed(description=f"{ctx.author.mention} Has to be more than 0 and less than 100 gems/ingots!~", guild=ctx.guild))
            return

        embed = utils.SpecialEmbed(author=f"Click the emote for currency type! (Thanks For Donating!)", desc=f"{silver_e} Silver\n{gold_e} Gold\n{emerald_e} Emerald\n{diamond_e} Diamond", guild=ctx.guild)
        msg = await ctx.send(embed=embed)

        # adds the reactions
        await msg.add_reaction(silver_e)
        await msg.add_reaction(gold_e)
        await msg.add_reaction(emerald_e)
        await msg.add_reaction(diamond_e)

        try:

            # Watches for the reactions
            check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and str(x.emoji) in [silver_e, gold_e, emerald_e, diamond_e]
            r, _ = await self.bot.wait_for('reaction_add', check=check)
            if str(r.emoji) == silver_e:
                await utils.GemFunction.pay_exchange(user=ctx.author)
                if c.silver < gems:
                    raise TooPoor
                c_r.silver += gems
                c.silver -= gems

            if str(r.emoji) == gold_e:
                await utils.GemFunction.pay_exchange(user=ctx.author)
                if c.gold < gems:
                    raise TooPoor
                c_r.gold += gems
                c.gold -= gems

            if str(r.emoji) == emerald_e:
                await utils.GemFunction.pay_exchange(user=ctx.author)
                if c.emerald < gems:
                    raise TooPoor
                c_r.emerald += gems
                c.emerald -= gems

            if str(r.emoji) == diamond_e:
                await utils.GemFunction.pay_exchange(user=ctx.author)
                if c.diamond < gems:
                    raise TooPoor
                c_r.diamond += gems
                c.diamond -= gems


        except TooPoor:
            await ctx.send(f'{ctx.author.mention} Payment denied. You would go in debt stupid!!!')
            return

        #! Always update after pay_exhange!
        await utils.GemFunction.update_gems(user=ctx.author)
        await utils.GemFunction.update_gems(user=receiver)

        async with self.bot.database() as db:
            await c.save(db)
            await c_r.save(db)

        await msg.delete()
        await ctx.send(embed=utils.SpecialEmbed(title=f"{ctx.author} Made a payment", desc=f"**{gems} {str(r.emoji)} was sent to {receiver}!**", guild=ctx.guild))

        log = await utils.ChannelFunction.get_log_channel(guild=ctx.guild, log="currency")
        await log.send(embed=utils.LogEmbed(type="positive", title=f"{ctx.author} made a payment.", desc=f"{ctx.author} payed {gems} {str(r.emoji)} was sent to {receiver}!", guild=ctx.guild))





def setup(bot):
    x = Payment(bot)
    bot.add_cog(x)