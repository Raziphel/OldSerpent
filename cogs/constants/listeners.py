# Discord
from discord.ext.commands import Cog

import utils


# Additions

class Listeners(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener('on_message')
    async def stream_ping(self, message):
        '''
        Ping when a streamer pings!
        '''
        if message.channel.id == 1051323487287005264:
            if message.author.id != 550474149332516881:
                await message.channel.send(f"<@&1070576949837180939>")


    @Cog.listener('on_message')
    async def vote_channels(self, message):
        '''
        Adds votes reactions!
        '''

        tr = utils.Tracking.get(message.author.id)
        tr.messages += 1
        async with self.bot.database() as db:
            await tr.save(db)

        # Check for general
        if message.channel.id in [1047026469068623902, 1056747785749278761, 1056776991770161162]: #? Suggestions
            await message.add_reaction("<:UpVote:1041606985080119377>")
            await message.add_reaction("<:DownVote:1041606970492342282>")
        if message.channel.id in [1051033412456165396]: #? 1 word only
            total_words = len(message.content.split())
            if total_words > 1 or list(message.content) in ["=", "-", "_", "~", "`", "."]:
                await message.delete()
                await message.channel.send(embed=utils.DefualtEmbed(title="1 Word Only!", desc="If it wasn't obvious you can only send 1 word."), delete_after=5)



    @Cog.listener()
    async def on_member_update(self, before, after):
        guild = self.bot.get_guild(self.bot.config['garden_id']) #? Guild
        if before.premium_since is None and after.premium_since is not None:
            c = utils.Currency(before.id)
            coin = self.bot.config['emotes']['coin']
            total_coins = 0
            try:
                await user.send(embed=utils.SpecialEmbed(title="- Nitro Rewards -", desc=f"A reward for being a nitro booster!\n\n**+5,000 {coin}**", footer=f"You can expect this reward every 30 days!"))
            except: pass
            c.coins += 5000
            total_coins += 5000
            for user in guild.members:
                nitro = utils.DiscordGet(guild.roles, id=self.bot.config['roles']['thaumiel'])
                if nitro in user.roles:
                    c = utils.Currency(user.id)
                    try:
                        await user.send(embed=utils.SpecialEmbed(title="- Nitro Rewards -", desc=f"A smaller reward becuase someone nitro boosted!\n\n**+1,000 {coin}**", footer=f"You can expect this reward every time someone boosts!"))
                    except: pass
                    c.coins += 1000
                    total_coins += 1000
                    async with self.bot.database() as db:
                        await c.save(db)

            supporters = self.bot.get_channel(self.bot.config['channels']['supporters'])
            await supporters.send(embed=utils.SpecialEmbed(desc=f"*All nitro boosters recieved a reward!\n**Total Coins:** {total_coins:,}", footer=f" "))


def setup(bot):
    x = Listeners(bot)
    bot.add_cog(x)
