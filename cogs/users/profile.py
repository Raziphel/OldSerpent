# * Discord
from discord.ext.commands import command, Cog, BucketType, cooldown, group, ApplicationCommandMeta
from discord import Member, Message, User, Game, User, ApplicationCommandOption, ApplicationCommandOptionType, File
# * Additions
from datetime import datetime as dt, timedelta
from asyncio import sleep
from math import floor
# * Utils
import utils

import asyncio

# Import the necessary modules
from playwright.async_api import async_playwright

profile_template = 'profile-template.html'


class Profile(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.browser = None
        self.bot.loop.create_task(self.bootstrap())

    async def bootstrap(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)

    @cooldown(1, 60, BucketType.channel)
    @command(
        aliases=['p', 'P', 'Profile'],
        application_command_meta=ApplicationCommandMeta(
            options=[
                ApplicationCommandOption(
                    name="user",
                    description="The user you want to get the profile of.",
                    type=ApplicationCommandOptionType.user,
                    required=False,
                ),
            ],
        ),
    )
    async def profile(self, ctx, user: Member = None):
        '''Shows a user's profile'''
        if not user:
            user = ctx.author

        # ! Quest 1 Complete
        # await self.bot.get_cog('Quests').get_quest(user=user, quest_no=1, completed=True)

        # await self.base_profile(ctx=ctx, user=user, msg=None)
        file = await self.generate_screenshot(user)

        await ctx.send(file=file)

    async def generate_screenshot(self, member: Member):
        def format_number(num):
            if num < 1000:
                return str(num)
            elif num < 1000000:
                return f"{num / 1000:.1f}K"
            elif num < 1000000000:
                return f"{num / 1000000:.1f}M"
            else:
                return f"{num / 1000000000:.1f}B"

        moderation = utils.Moderation.get(member.id)
        levels = utils.Levels.get(member.id)
        currency = utils.Currency.get(member.id)
        tracking = utils.Tracking.get(member.id)
        staff_tracking = utils.Staff_Track.get(member.id)

        if levels.level == 0:
            required_exp = 10
        elif levels.level < 5:
            required_exp = levels.level * 25
        else:
            required_exp = round(levels.level ** 2.75)

        current_experience = floor(levels.exp)
        experience_percentage = floor(current_experience / required_exp) * 100

        voice_days = floor((tracking.vc_mins / 60) / 24)

        # Create a new page and set the HTML content of the page
        page = await self.browser.new_page()

        page.on("request", lambda request: print(">>", request.method, request.url))
        page.on("response", lambda response: print("<<", response.status, response.url))

        # Read HTML from the template
        with open('profile-template.html', 'r') as html_template_hdl:
            html_template = html_template_hdl.read()
            html_template = html_template.format(
                level=levels.level,
                progress=experience_percentage,
                experience=f'{current_experience:,}/{required_exp:,}',
                coins=format_number(currency.coins),
                messages=format_number(tracking.messages),
                voice=format_number(voice_days)
            )

        await page.set_content(html_template)

        screenshot_buffer = await page.locator('.outer-rectangle').screenshot()
        file = File(screenshot_buffer, filename='profile.png')

        return file

    async def base_profile(self, ctx, user, msg):
        if msg == None:
            msg = await ctx.send(embed=utils.ProfileEmbed(type="Default", user=user))
        else:
            await msg.edit(embed=utils.ProfileEmbed(type="Default", user=user))

        await msg.clear_reactions()
        # ! adds the reactions
        if ctx.channel.id in self.bot.config['fur-channels'].values():
            await msg.add_reaction("✨")
        if ctx.channel.id in self.bot.config['nsfw-fur-channels'].values():
            await msg.add_reaction("🔞")
        # for role in user.roles:
        #     if role.id == self.bot.config['roles']['council']:
        #         await msg.add_reaction("🍃")

        # Watches for the reactions
        check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and x.emoji in ["✨", "🍃"]
        r, _ = await self.bot.wait_for('reaction_add', check=check)
        if ctx.channel.id in self.bot.config['fur-channels'].values():
            if r.emoji == "✨":
                await msg.edit(embed=utils.ProfileEmbed(type="Sfw_Sona", user=user))
                pass
        if r.emoji == "🍃":
            await msg.edit(embed=utils.ProfileEmbed(type="Staff-Track", user=user))
            pass
        await msg.clear_reactions()
        await msg.add_reaction("🔷")
        check = lambda x, y: y.id == ctx.author.id and x.message.id == msg.id and x.emoji in ["🔷"]
        r, _ = await self.bot.wait_for('reaction_add', check=check)
        if r.emoji == "🔷":
            await self.base_profile(ctx=ctx, user=user, msg=msg)
            return

    @cooldown(1, 30, BucketType.user)
    @command(aliases=['Sona', 'fursona', 'Fursona'])
    async def sona(self, ctx, user: Member = None):
        '''Quick Post Sona'''
        if ctx.channel.id in self.bot.config['fur-channels'].values():
            await ctx.send("You can't post that nasty-ness here.", delete_after=10)
            await ctx.message.delete()
            return
        if not user:
            user = ctx.author
        m = await ctx.send(embed=utils.ProfileEmbed(type="Sfw_Sona", user=user, quick=True))

<<<<<<< Updated upstream
    @cooldown(1, 30, BucketType.user)
    @command(aliases=['NSona', 'nfursona', 'nFursona'])
    async def nsona(self, ctx, user:Member=None):
        '''Quick Post Nsfw Sona'''
        if ctx.channel.id in self.bot.config['nsfw-fur-channels'].values():
            await ctx.send("You can't post that nasty-ness here.", delete_after=10)
            await ctx.message.delete()
            return
        if not user:
            user = ctx.author
        m = await ctx.send(embed=utils.ProfileEmbed(type="Nsfw_Sona", user=user, quick=True))


    @cooldown(1, 30, BucketType.user)
    @command(aliases=['c', 'C', 'Gems', 'ingots', 'gems', 'Ingots'])
    async def currency(self, ctx, user:Member=None):
        '''Quick Check Gems'''
        if not user:
            user = ctx.author
        m = await ctx.send(embed=utils.ProfileEmbed(type="Currency", user=user, quick=True))



=======
>>>>>>> Stashed changes
    @cooldown(1, 5, BucketType.user)
    @command(aliases=['color', 'Color', 'Setcolor', 'SetColor'])
    async def setcolor(self, ctx, colour):
        '''Sets your user color'''
<<<<<<< Updated upstream
        colour_value = utils.Colors.get(colour.lower()) 
        ss = utils.Settings.get(ctx.author.id)
=======
        colour_value = utils.Colors.get(colour.lower())
        ss = utils.Tracking.get(ctx.author.id)
>>>>>>> Stashed changes

        if colour_value == None:
            try:
                colour_value = int(colour.strip('#'), 16)
            except ValueError:
<<<<<<< Updated upstream
                await ctx.send(embed=utils.SpecialEmbed(title="Incorrect colour usage!", guild=ctx.guild), delete_after=15)
=======
                await ctx.send(embed=utils.SpecialEmbed(title="Incorrect colour usage!", guild=ctx.guild),
                               delete_after=5)
>>>>>>> Stashed changes
                return

        ss.color = colour_value
        async with self.bot.database() as db:
            await ss.save(db)
<<<<<<< Updated upstream
        
        await ctx.send(embed=utils.DefualtEmbed(title="Your color setting has been set!", guild=ctx.guild, user=ctx.author), delete_after=15)

=======
>>>>>>> Stashed changes

        await ctx.send(
            embed=utils.DefualtEmbed(title="Your color setting has been set!", guild=ctx.guild, user=ctx.author))


def setup(bot):
    x = Profile(bot)
    bot.add_cog(x)
