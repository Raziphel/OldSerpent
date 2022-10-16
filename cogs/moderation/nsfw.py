
#* Discord
from discord.ext.commands import command, Cog, Greedy
from discord import Member, Message, User

import utils

class Nsfw(Cog):
    def __init__(self, bot):
        self.bot = bot


    @property  #! The members logs
    def members_log(self):
        return self.bot.get_channel(self.bot.config['members_log']) 



    @utils.is_mod_staff()
    @command()
    async def notnsfw(self, ctx, user:Member):
        '''Removes nsfw access from a user!'''
        await self.notnsfw_user(guild=guild, user=user)
        st = utils.Staff_Track.get(ctx.author.id)
        st.purges += 1
        async with self.bot.database() as db:
            await st.save(db)
        await ctx.send(embed=utils.WarningEmbed(title=f"{user.mention}, has been NSFW restricted!", guild=ctx.guild))

    async def notnsfw_user(self, guild, user:Member):
        role = utils.DiscordGet(guild.roles, name="Adult 🚬")
        mod = utils.Moderation.get(user.id)
        try: #! Removes 18+ role if exists!
            await user.remove_roles(role)
        except: pass
        role = utils.DiscordGet(user.guild.roles, name="Child 🍼")
        await user.add_roles(role)
        mod.nsfw = True
        async with self.bot.database() as db:
            await mod.save(db)
        #! Log the action!
        await self.members_log.send(embed=utils.LogEmbed(type="negative", title=f"NSFW Restricted", desc=f"{user.name} was nsfw restricted!", guild=guild))




    @utils.is_mod_staff()
    @command()
    async def nsfw(self, ctx, user:Member):
        '''Add nsfw access from a user!'''
        await self.nsfw_user(user=user, guild=ctx.guild)
        st = utils.Staff_Track.get(ctx.author.id)
        st.purges += 1
        async with self.bot.database() as db:
            await st.save(db)
        await ctx.send(embed=utils.WarningEmbed(title=f"{user.mention}, has been allowed NSFW!  Happy Birthday, probably.", guild=guild))

    async def nsfw_user(self, user:Member, guild):
        role = utils.DiscordGet(guild.roles, name="Child 🍼")
        mod = utils.Moderation.get(user.id)
        mod.nsfw = False
        async with self.bot.database() as db:
            await mod.save(db)
        #! Report and log the action!
        await self.members_log.send(embed=utils.LogEmbed(type="positive", title=f"NSFW Allowed", desc=f"{user.name} was allowed nsfw access!"))




def setup(bot):
    x = Nsfw(bot)
    bot.add_cog(x)