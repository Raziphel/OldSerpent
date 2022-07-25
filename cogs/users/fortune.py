# Discord
from discord.ext.commands import command, Cog
from discord import Member
# Additions
from random import choice
from time import monotonic

# Utils
import utils

class fortune(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.YesorNo = ([
            "Yes, but that's gross!",
            "No. Your a loser! >;c",
            "I can't answer stupidity.",
            "Yeah, but thats really stupid!",
            "No, you nasty furry~",
            "Eww wtf. Hell no!",
            "Only a homosexual would ask that.",
            "I was told to say No.",
            "I was told to say Yes.",
            "Wtf?  Yeah fuck no.",
            "Oh fuck.  Fuck Yes.",
            "Yeah, but you need jesus...",
            "No x100!  Thats horrible.",
            "Why ofcourse you fag~",
            "Yeah no.  100% not!",
            "Wow, hell no! settle down there faggot!",
            "No, thank you. But that's gross.",
            "Yeah, but your probably gonna get a disease...",
            "Are you gay? Then maybe...",
            "Yes, but you'll get cancer",
            "Yes but your lover will harass you.",
            "Oh my fucking god, yes!", 
            "Yes, but only if it's tuesday.", 
            "What are you talking about? Of course not!?",  
            "The answer is yes, but your gay af for asking.", 
            "Never going to happen! Ever!", 
            "Nope, never!", 
            "Yes, but get drunk af first!", 
            "Only if you eat ass while doing it.", 
            "Probably, yeah?",
            "Oh baby.  You better believe it.",
            "It's a high likelyhood!",
            "Yikes, how about no.",
            "Yoooooo, hell no, settle down.",
            "Omfg, yeah thats a big fat no.",
            "Wtf, yeah why not.",
            "C'mon you already know thats a no.",
            "You ask too many questions, but no.",
            "Sometimes...",
            "Without a doubt thats a no.",
            "Hell no, to the no.",
            "Yeah for sure.",
            "Shut the hell up, ofcourse."
        ])

        self.Nwords = ([
            "Nuzzles", 
            "Nails", 
            "Nerds", 
            "Neat", 
            "Naked", 
            "Neighbor", 
            "Negative", 
            "Neck", 
            "Near", 
            "Natural", 
            "Nausea", 
            "Nigeria", 
            "Never", 
            "Niggles", 
            "Nickles",
            "Nothing", 
            "Niagra Falls", 
            "No", 
            "Narwhal", 
            "Nicotine", 
            "Nutrition", 
            "Nobel", 
            "Nostril", 
            "Nugget", 
            "Nesquik", 
            "Nasty",
            "Naplm",
            "Nutela",
            "Nuetral",
            "Neptune",
            "Neil Armstrong",
            "Nether",
            "Noob",
        ])


    @command(aliases=['8ball', 'ask', 'Ask', 'Fortune'])
    async def fortune(self, ctx, args):
        '''
        Tells people there fortunes
        '''
        contents = ctx.message.content.split()
        total_words = len(ctx.message.content.split())
        response = "I don't understand that question~"

        for word in contents:
            if word.lower() in ["am", "will", "does", "should", "can", "are", "do", "is"]:
                response = choice(self.YesorNo)

        await ctx.send(embed=utils.DefualtEmbed(desc=response))


    @command()
    async def nword(self, ctx):
        '''
        Gives a random N word
        '''

        response = choice(self.Nwords)

        await ctx.send(embed=utils.DefualtEmbed(desc=response))


    # @is_donator_general()
    # @commands.command()
    # async def response(self, ctx, *, response:str):
    #     '''
    #     Sends a suggestion for the fortune command
    #     '''

    #     ss= utils.Settings.get(ctx.author.id)
    #     channel = self.bot.get_channel(self.bot.config['channels']['razi_realm'])
    #     embed=discord.Embed(description="{}".format(response), color=uc.colour)
    #     embed.set_author(name="Reponse Idea:")
    #     embed.set_footer(icon_url=ctx.author.avatar_url, text="Response from: {}".format(ctx.author.display_name)) 
    #     await channel.send(embed=embed)

    #     embed2=discord.Embed(description="**Your response idea has been sent!**", color=uc.colour)
    #     msg = await ctx.send(embed=embed2)
    #     await asyncio.sleep(3)
    #     await ctx.message.delete()
    #     await msg.delete()

    @Cog.listener('on_message')
    async def yeet(self, message):
        '''
        Weed
        '''
        if 'weed' in message.content.lower():
            await message.add_reaction('<:Weed:702577534117871718>')
        return












def setup(bot):
    x = fortune(bot)
    bot.add_cog(x)