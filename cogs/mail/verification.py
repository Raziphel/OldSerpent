
#* Discord
from discord.ext.commands import Cog
from discord import Embed, Member, DiscordException, guild
#* Additions
from asyncio import TimeoutError
from typing import Optional

import utils
# * Additions
from asyncio import TimeoutError
from typing import Optional

from discord import Embed, Member, DiscordException, guild
from discord.ext.commands import Cog

import utils


class VerificationCancelled(BaseException):
    pass


class Verification(Cog):

    def __init__(self, bot):
        self.bot = bot


    @property  #! The currency logs
    def mailbox(self):
        return self.bot.get_channel(self.bot.config['channels']['mail_box']) #?archive log channel






    async def verification(self, author:Member, guild:guild):
        '''Sends a verification application!'''

        # Set some stuff up
        table_data = {
            'invited': None,
            'reason': None,
            'age': None,
        }


        async def get_input(prompt: str, timeout: float = 360.0, max_length: Optional[int] = 50):
            '''Gets users responses and checks them'''
            await author.send(embed=utils.SpecialEmbed(desc=prompt, footer=" ", guild=guild))

            async def get_response():
                ''''Waits for users responses'''
                msg = await self.bot.wait_for('message', check=lambda m: m.author.id == author.id and not m.guild, timeout=timeout)

                if 'cancel' == msg.content.lower():
                    raise VerificationCancelled

                return msg

            message = await get_response()

            if max_length is not None:
                while len(message.content) > max_length:
                    await author.send(f"Sorry, but the value you've responded with is too long. Please keep it within {max_length} characters.")
                    message = await get_response()

            return message

        try:
            invited = await get_input(f"Where did you recieve an invintation to {guild.name} from?")
            table_data['invited'] = invited.content

            reason = await get_input(f"What is your reason for joining {guild.name}?")
            table_data['reason'] = reason.content

            age = await get_input("How old are you?")
            table_data['age'] = age.content

            color = await get_input("What's your favourite colour? (Say a color name or a hex code)")
            colour_value = utils.Colors.get(color.content.lower()) 
            if colour_value == None:
                try:
                    colour_value = int(color.content.strip('#'), 16)
                except ValueError:
                    pass
            tr = utils.Tracking.get(author.id)
            tr.color = colour_value
            async with self.bot.database() as db:
                await tr.save(db)

            if color is None:
                color = 0x0
                await author.send('Invalid color specified, setting to default.')

            msg = f"How they were invited: **{table_data.get('invited')}**\nReason For Joining: **{table_data.get('reason')}**\nAge: **{str(table_data.get('age'))}**"

            msg = await self.mailbox.send(embed=utils.MailEmbed(title=f"Razi's Realm Application", footer=f"Verification", message=msg, color=tr.color, author=author, image=author.avatar.url))
            await msg.add_reaction('✅')
            await msg.add_reaction('🔴')

            embed2=Embed(description="**Your verification has been sent!**")
            await author.send(embed=embed2)

        except DiscordException:
            await author.send('I\'m unable to DM you?')

        except VerificationCancelled:
            await author.send('Aborting Verification!')

        except TimeoutError:
            await author.send('Sorry, but you took too long to respond.  Verification has closed.')





    async def verify_furry(self, author:Member, guild:guild):
        '''Sends a kingussy verification application!'''

        # Set some stuff up
        table_data = {
            'furry': None,
            'sona': None,
            'reason': None,
            'drama': None,
        }


        async def get_input(prompt: str, timeout: float = 360.0, max_length: Optional[int] = 50):
            '''Gets users responses and checks them'''
            await author.send(embed=utils.SpecialEmbed(desc=prompt, footer=" ", guild=guild))

            async def get_response():
                ''''Waits for users responses'''
                msg = await self.bot.wait_for('message', check=lambda m: m.author.id == author.id and not m.guild, timeout=timeout)

                if 'cancel' == msg.content.lower():
                    raise VerificationCancelled

                return msg

            message = await get_response()

            if max_length is not None:
                while len(message.content) > max_length:
                    await author.send(f"Sorry, but the value you've responded with is too long. Please keep it within {max_length} characters.")
                    message = await get_response()

            return message

        try:
            furry = await get_input(f"Are you a furry?")
            table_data['furry'] = furry.content

            sona = await get_input(f"Tell me about your sona!")
            table_data['sona'] = sona.content

            reason = await get_input(f"What made you decide to join this server?")
            table_data['reason'] = reason.content

            drama = await get_input(f"Are you a fan of drama?")
            table_data['drama'] = drama.content

            msg = f"A furry?: **{table_data.get('furry')}**\nSona?: **{table_data.get('sona')}**\nReason?: **{table_data.get('reason')}**\nDrama?: **{table_data.get('drama')}**"

            msg = await self.mailbox.send(embed=utils.MailEmbed(title=f"Furry Application", footer=f"Furry", message=msg, color=tr.color, author=author, image=author.avatar.url))
            await msg.add_reaction('✅')
            await msg.add_reaction('🔴')

            embed2=Embed(description="**Your verification has been sent!**")
            await author.send(embed=embed2)

        except DiscordException:
            await author.send('I\'m unable to DM you?')

        except VerificationCancelled:
            await author.send('Aborting Furry Verification!')

        except TimeoutError:
            await author.send('Sorry, but you took too long to respond.  Verification has closed.')






    async def verify_adult(self, author:Member, guild:guild, kinda:bool=False):
        '''Sends a adult verification application!'''

        # Set some stuff up
        table_data = {
            'proof': None,
        }


        async def get_input(prompt: str, timeout: float = 360.0, max_length: Optional[int] = 50):
            '''Gets users responses and checks them'''
            await author.send(embed=utils.SpecialEmbed(desc=prompt, footer=" ", guild=guild))

            async def get_response():
                ''''Waits for users responses'''
                msg = await self.bot.wait_for('message', check=lambda m: m.author.id == author.id and not m.guild, timeout=timeout)

                if 'cancel' == msg.content.lower():
                    raise VerificationCancelled

                return msg

            message = await get_response()

            if max_length is not None:
                while len(message.content) > max_length:
                    await author.send(f"Sorry, but the value you've responded with is too long. Please keep it within {max_length} characters.")
                    message = await get_response()

            return message

        try:
            proof = await get_input(f"**Lying about your age is a bannable offense!\n\nWe take this rule very seriously and once we find out you are child you will be banned and reported to Discord.**\n\nPlease say `I agree` if you are indeed an adult or do `cancel`.")
            table_data['proof'] = proof.content

            msg = f"**Marked Child?**: {mod.child}\n**Agreement:** {table_data.get('proof')}"

            tr = utils.Tracking.get(author.id)
            mod = utils.Moderation.get(author.id)
            footer = "Adult"
            msg = await self.mailbox.send(embed=utils.MailEmbed(title=f"Adult Application", footer=footer, message=msg, color=tr.color, author=author, image=author.avatar.url))
            await msg.add_reaction('✅')
            await msg.add_reaction('🔴')

            embed2=Embed(description="**Your Adult verification has been sent!**")
            await author.send(embed=embed2)

        except DiscordException:
            await author.send('I\'m unable to DM you?')

        except VerificationCancelled:
            await author.send('Aborting Adult Verification!')

        except TimeoutError:
            await author.send('Sorry, but you took too long to respond.  Verification has closed.')







def setup(bot):
    x = Verification(bot)
    bot.add_cog(x)