
#* Discord
from discord.ext.commands import command, Cog
from discord import Embed, PartialEmoji, Message, Member, DiscordException, guild
#* Additions
from asyncio import sleep, TimeoutError
from typing import Optional
from re import findall

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


        async def get_input(prompt: str, timeout: float = 120.0, max_length: Optional[int] = 50):
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
            ss = utils.Settings.get(author.id)
            ss.color = colour_value
            async with self.bot.database() as db:
                await ss.save(db)

            if color is None:
                color = 0x0
                await author.send('Invalid color specified, setting to default.')

            msg = f"How they were invited: **{table_data.get('invited')}**\nReason For Joining: **{table_data.get('reason')}**\nAge: **{str(table_data.get('age'))}**"

            msg = await self.mailbox.send(embed=utils.MailEmbed(footer=f"Verification", message=msg, color=ss.color, author=author, image=author.avatar_url))
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





    async def verify_kingussy(self, author:Member, guild:guild):
        '''Sends a kingussy verification application!'''

        # Set some stuff up
        table_data = {
            'password': None,
            'username': None,
        }


        async def get_input(prompt: str, timeout: float = 120.0, max_length: Optional[int] = 50):
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
            password = await get_input(f"Whats the password for access?")
            table_data['password'] = password.content

            username = await get_input(f"Whats your username in Grepolis?")
            table_data['username'] = username.content


            color = await get_input("What's your favourite colour? (Say a color name or a hex code)")
            colour_value = utils.Colors.get(color.content.lower()) 
            if colour_value == None:
                try:
                    colour_value = int(color.content.strip('#'), 16)
                except ValueError:
                    pass
            ss = utils.Settings.get(author.id)
            ss.color = colour_value
            async with self.bot.database() as db:
                await ss.save(db)

            if color is None:
                color = 0x0
                await author.send('Invalid color specified, setting to default.')

            msg = f"Password: **{table_data.get('password')}**\nGrepolis Username: **{table_data.get('username')}**"

            msg = await self.mailbox.send(embed=utils.MailEmbed(footer=f"Kingussy", message=msg, color=ss.color, author=author, image=author.avatar_url))
            await msg.add_reaction('✅')
            await msg.add_reaction('🔴')

            embed2=Embed(description="**Your verification has been sent!**")
            await author.send(embed=embed2)

        except DiscordException:
            await author.send('I\'m unable to DM you?')

        except VerificationCancelled:
            await author.send('Aborting Alliance Verification!')

        except TimeoutError:
            await author.send('Sorry, but you took too long to respond.  Verification has closed.')




def setup(bot):
    x = Verification(bot)
    bot.add_cog(x)