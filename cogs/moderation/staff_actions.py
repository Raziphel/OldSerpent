
#* Discord
from discord.ext.commands import command, Cog, Greedy
from discord import Member, Message, User, Embed

#* Additions
from typing import Optional
from asyncio import sleep
from datetime import datetime as dt, timedelta
from random import choice

import utils

class Staff_Actions(Cog):
    def __init__(self, bot):
        self.bot = bot


    @property  #! The message logs
    def message_log(self):
        return self.bot.get_channel(self.bot.config['message_log']) 


    @utils.is_mod_staff()
    @command(aliases=['prune'])
    async def purge(self, ctx, user:Optional[User], amount:int=10):
        '''Purges the given amount of messages from the channel.'''   
        if user:
            check = lambda m: m.author.id == user.id
        else:
            check = lambda m: True

        #! Add max amount
        if amount > 250:
            await ctx.send(f"**250 is the maxium amount of messages.**")
            return

        #! Report and log the purging!
        st = utils.Staff_Track.get(ctx.author.id)
        st.purges += 1
        async with self.bot.database() as db:
            await st.save(db)
        removed = await ctx.channel.purge(limit=amount, check=check)
        await ctx.send(embed=utils.SpecialEmbed(title=f"Deleted {len(removed)} messages!", guild=ctx.guild))
        await self.message_log.send(embed=utils.LogEmbed(type="negative", title=f"Channel messages Purged", desc=f"<@{ctx.author.id}> purged {amount} messages from <#{ctx.channel.id}>!"))


    @utils.is_mod_staff()
    @command(aliases=['cl'])
    async def clean(self, ctx):
        '''Clears the bot's messages!'''
        check = lambda m: m.author.id == self.bot.user.id or m.id == ctx.message.id or m.content.startswith(self.bot.config['prefix']) 
        await ctx.channel.purge(check=check)


    @utils.is_mod_staff()
    @command(aliases=['whos'])
    async def whois(self, ctx, user:Member=None):
        '''Gives information on the user!'''
        if not user:
            user = ctx.author
        embed=Embed(title=f"{user}'s Member Information", description=f"", color=0x1d89e3)
        created_at = user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        joined_at = user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        embed.add_field(name="Joined", value=f'{joined_at}', inline=True)
        embed.add_field(name="Registered", value=f'{created_at}', inline=True)
        roles = []
        for i in user.roles:
            roles.append(f"{i.mention}")
        role_string = ', '.join(roles)
        embed.add_field(name=f"Roles [{len(user.roles)}]", value=f'{role_string}', inline=False)
        perm_list = [perm[0] for perm in user.guild_permissions if perm[1]]
        perm_string = ', '.join(perm_list)
        embed.add_field(name=f"Perm-Level", value=f'{perm_string}', inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    x = Staff_Actions(bot)
    bot.add_cog(x)