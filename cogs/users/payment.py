# Discord
from discord import User, ApplicationCommandOption, ApplicationCommandOptionType
from discord.ext.commands import command, cooldown, BucketType, Cog, ApplicationCommandMeta

# Utils
import utils


class Payment(Cog):
    def __init__(self, bot):
        self.bot = bot

    @property  # ! The members logs
    def coin_logs(self):
        return self.bot.get_channel(self.bot.config['channels']['coin_logs'])  # ?Coins log channel

    @cooldown(1, 30, BucketType.user)
    @command(
        aliases=['send'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="recipient",
                    description="The user you want to send coins to.",
                    type=ApplicationCommandOptionType.user,
                    required=True,
                ),
                ApplicationCommandOption(
                    name="amount",
                    description="The amount of coins you'd like to send.",
                    type=ApplicationCommandOptionType.integer,
                    required=True,
                ),
            ],
        ),
    )
    async def pay(self, ctx, recipient: User = None, amount: int = 0):
        """Send a payment to another member."""
        coin_e = self.bot.config['emotes']['coin']

        # Check if the recipient is the same as the user.
        if recipient == ctx.author:
            return await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(description=f"{ctx.author} You can't pay yourself coins! stupid..."))

        if amount <= 10:
            return await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(description=f"{ctx.author} Has to be more than 10!"))

        # Check if the user has enough coins.
        c = utils.Currency.get(ctx.author.id)
        if amount > c.coins:
            return await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(description=f"{recipient.mention} you don't have that many coins."))

        await utils.CoinFunctions.pay_user(payer=ctx.author, receiver=recipient, amount=amount)

        await ctx.interaction.response.send_message(embed=utils.DefaultEmbed(description=f"**{ctx.author} sent {amount:,}x {coin_e} to {recipient}!**"))

        await self.coin_logs.send(f"**{ctx.author}** payed **{amount} {coin_e}** to **{recipient}**!")


def setup(bot):
    x = Payment(bot)
    bot.add_cog(x)
