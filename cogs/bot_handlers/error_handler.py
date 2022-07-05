
#* Discord
from discord.ext.commands import command, Cog
from discord.ext.commands import MissingRequiredArgument, BadArgument, CommandNotFound, CheckFailure, CommandInvokeError, CommandOnCooldown, NotOwner, MissingPermissions
#* Utils
import utils
#* Additions
from asyncio import sleep

class Error_Handler(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_command_error(self, ctx, error):
        '''Globally handles errors around the bot'''


        if isinstance(error, CommandOnCooldown):
            countdown_time = error.retry_after
            for role in ctx.author.roles:
                if role.name in self.bot.supporters:
                    await ctx.send("`Bypassing Cooldown, Thanks for supporting!`")
                    await ctx.reinvoke()
                    break
            else:
                if countdown_time <= 60:
                    msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"CommandOnCooldown", desc=f"Oi, your on cooldown try again in {countdown_time:.2f} seconds!"))
                else:
                    msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=f"CommandOnCooldown", desc=f"Oi, your on cooldown try again in {countdown_time // 60:.0f} minutes {countdown_time % 60:.0f} seconds!"))
                    pass

        elif isinstance(error, CommandNotFound):
            return
        elif isinstance(error, MissingPermissions):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=self.bot.config['messages']['errors']['missing_permissions']))
            pass
        elif isinstance(error, BadArgument):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=self.bot.config['messages']['errors']['bad_arguments']))
            pass
        elif isinstance(error, utils.InDmsCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=self.bot.config['messages']['errors']['in_dms']))
            pass
        elif isinstance(error, utils.UserCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=self.bot.config['messages']['errors']['user_error']))
            pass
        elif isinstance(error, utils.DevCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=self.bot.config['messages']['errors']['dev_error']))
            pass
        elif isinstance(error, utils.GuildCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=self.bot.config['messages']['errors']['guild_check']))
            pass
        elif isinstance(error, utils.ModStaffCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=self.bot.config['messages']['errors']['mod_check']))
            pass
        elif isinstance(error, utils.AdminStaffCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=self.bot.config['messages']['errors']['admin_check']))
            pass
        elif isinstance(error, utils.OwnerStaffCheckError):
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=self.bot.config['messages']['errors']['owner_check']))
            pass
        else: 
            msg = await ctx.send(embed=utils.ErrorEmbed(error_msg=self.bot.config['messages']['errors']['error']))
            pass

        if ctx.author.id == self.bot.config['developer']:
            await ctx.author.send(f"Command failed - `{error!s}`;")

        await sleep(4)
        await msg.delete()
        await ctx.message.delete()

def setup(bot):
    x = Error_Handler(bot)
    bot.add_cog(x)
