
#* Discord
from discord.ext.commands import command, Cog, Greedy
from discord import Member, Message, User

import utils

class Nsfw(Cog):
    def __init__(self, bot):
        self.bot = bot



    @utils.is_mod_staff()
    @command()
    async def notnsfw(self, ctx, user:Member):
        '''Removes nsfw access from a user!'''
        await self.notnsfw_user(guild=guild, user=user)
        await ctx.send(embed=utils.WarningEmbed(title=f"{user.mention}, has been NSFW restricted!", guild=ctx.guild))

    async def notnsfw_user(self, guild, user:Member):
        if guild.id == self.bot.config['guilds']['RaziRealmID']:
            role = utils.DiscordGet(guild.roles, name="Adult 🚬")
        elif guild.id == self.bot.config['guilds']['FurryRoyaleID']:
            role = utils.DiscordGet(guild.roles, name="18+")

        mod = utils.Moderation.get(user.id)
        try: #! Removes 18+ role if exists!
            await user.remove_roles(role)
        except: pass
        #! Add the jailbait role and update nsfw!
        if guild.id == self.bot.config['guilds']['RaziRealmID']:
            role = utils.DiscordGet(user.guild.roles, name="Child 🍼")
            await user.add_roles(role)
        mod.nsfw = True
        async with self.bot.database() as db:
            await mod.save(db)
        #! Log the action!
        log = await utils.ChannelFunction.get_log_channel(guild=member.guild, log="member")
        await log.send(embed=utils.LogEmbed(type="negative", title=f"NSFW Restricted", desc=f"{user.name} was nsfw restricted!", guild=guild))




    @utils.is_mod_staff()
    @command()
    async def nsfw(self, ctx, user:Member):
        '''Add nsfw access from a user!'''
        await self.nsfw_user(user=user, guild=ctx.guild)
        await ctx.send(embed=utils.WarningEmbed(title=f"{user.mention}, has been allowed NSFW", guild=guild))

    async def nsfw_user(self, user:Member, guild):
        if guild.id == self.bot.config['guilds']['RaziRealmID']:
            role = utils.DiscordGet(guild.roles, name="Child 🍼")
        mod = utils.Moderation.get(user.id)
        mod.nsfw = False
        async with self.bot.database() as db:
            await mod.save(db)
        #! Report and log the action!
        log = await utils.ChannelFunction.get_log_channel(guild=member.guild, log="member")
        await log.send(embed=utils.LogEmbed(type="positive", title=f"NSFW Allowed", desc=f"{user.name} was allowed nsfw access!"))




def setup(bot):
    x = Nsfw(bot)
    bot.add_cog(x)