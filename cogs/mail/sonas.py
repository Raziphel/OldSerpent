
#* Discord
from discord.ext.commands import command, Cog
from discord import Embed, PartialEmoji, Message, Member, DiscordException, guild
#* Additions
from asyncio import sleep, TimeoutError
from typing import Optional
from re import findall, compile

import utils



class SonaCancelled(BaseException):
    pass



def validate_image(message):
    if message.attachments:
        try:
            return message.attachments[0].url
        except KeyError:
            return None

    uri = message.content.split()[0]
    valid_uri = compile(r"(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")

    if valid_uri.match(uri):
        return uri

    return None



class Sonas(Cog):
    def __init__(self, bot):
        self.bot = bot




    @property  #! The Server logs
    def bot_log(self):
        return self.bot.get_channel(self.bot.config['channels']['bot']) 

    @property 
    def mail_box(self):
        return self.bot.get_channel(self.bot.config['channels']['mail_box'])



    @command(aliases=['createsona', 'Setsona', 'sets'])
    async def setsona(self, ctx):
        '''Dms the sona creation prompt'''

        await ctx.message.add_reaction('👌')

        #! Define varibles
        guild = ctx.guild
        author = ctx.author

        # Set some stuff up
        table_data = {
            'type': None,
            'name': None,
            'gender': None,
            'sexuality': None,
            'age': None,
            'bio': None,
            'image': None,
            'species': None,
            'color': None,
            'likes': None,
            'nsfw': None,
        }

        async def get_input(prompt: str, timeout: float = 120.0, max_length: Optional[int] = 25):
            '''Gets users responses and checks them'''
            await author.send(embed=utils.SpecialEmbed(desc=prompt, footer=" ", guild=guild))

            async def get_response():
                ''''Waits for users responses'''
                msg = await self.bot.wait_for('message', check=lambda m: m.author.id == author.id and not m.guild, timeout=timeout)

                if 'cancel' == msg.content.lower():
                    raise SonaCancelled

                return msg

            message = await get_response()

            if max_length is not None:
                while len(message.content) > max_length:
                    await author.send(f"Sorry, but the value you've responded with is too long. Please keep it within {max_length} characters.")
                    message = await get_response()

            return message

        try:
            sona_nsfw = await get_input(f"**Welcome to sona creation!**\n\nIs this a NSFW sona? (Yes or No are valid responses.)")
            if sona_nsfw.content.lower() == "yes":
                nsfw = True
            elif sona_nsfw.content.lower() == "no":
                nsfw = False
            else:
                await author.send(f"That wasn't a correct response.")

            table_data['nsfw'] = nsfw

            role = guild.get_role(self.bot.config['roles']['nsfw_adult'])
            member = guild.get_member(ctx.author.id)
            if table_data['nsfw'] == 'yes' and role not in member.roles:
                    await author.send('**Sorry, but you need to be 18+ in order to submit a NSFW fursona.**')
                    return


            #! Get the sona's name
            name = await get_input(f"What is your sona's name?")
            table_data['name'] = name.content

            #! Get the sona's gender
            gender = await get_input(f"What is your sona's gender?")
            table_data['gender'] = gender.content

            #! Get the sona's sexuality
            sexuality = await get_input("Whats your sona's sexuality?")       
            table_data['sexuality'] = sexuality.content

            #! Get the sona's species
            species = await get_input("Whats your sona's species?")       
            table_data['species'] = species.content

            #! Get the sona's age
            age = await get_input("Whats your sona's age in years?")
            try:
                table_data['age'] = int(''.join([i for i in age.content if i.isdigit()]))
            except ValueError:
                response = await get_input("Sorry, but that isn't a number?  what is your sona's age in years?")
                table_data['age'] = int(''.join([i for i in response.content if i.isdigit()]))

            #! None of that shit
            if table_data['age'] < 18 and table_data['type'] == 'nsfw':
                await ctx.author.send('Underage NSFW fursonas are NOT allowed.  Unsuprisingly. Star over.')
                return

            #! Get the sona's color
            color = await get_input("What is your sona's favorite color? (Can be a color code or name of color.  Have over 200 color names)")
            if color.content.lower() != "none":
                color = utils.Colors.get(color.content.lower()) 
            else:
                try:
                    color = int(color.content.strip('#'), 16)
                except ValueError:
                    color = await get_message("**I don't know that color and I most colors...**")
            table_data['color'] = color

            #! Get the sona's likes
            likes = await get_input("List some things your sona likes!")       
            table_data['likes'] = likes.content
            if likes.content.lower() == 'none':
                table_data['likes'] = "Nothing..."

            #! Get the sona's bio
            bio = await get_input("What is your fursona's bio, if you have one (otherwise say `none`)? You have 20 minutes to write this before it times out automatically.", timeout=1200.0, max_length=1024)
            table_data['bio'] = bio.content.strip()
            if bio.content.lower() == 'none':
                table_data['bio'] = None

            #! Get the sona's image
            image = await get_input("Post a link your fursona's image if you have one (otherwise say `none`).", max_length=None)
            if image.content.lower() == 'none':
                table_data['image'] = None
            else:
                image_url = validate_image(image)
                while image_url is None:
                    image = await get_input("I couldn't validate the URL given to me, please try again (or say `none`).", max_length=None)
                    if image.content.lower() == 'none':
                        table_data['image'] = None
                        break
                    image_url = validate_image(image)
                if image_url is not None:
                    table_data['image'] = image_url


            if table_data['nsfw'] == True:
                sona = utils.Nsfw_sonas.get(author.id)
            else: 
                sona = utils.Sonas.get(author.id)

            sona.name = table_data.get('name')
            sona.gender = table_data.get('gender')
            sona.sexuality = table_data.get('sexuality')
            sona.age = int(table_data.get('age'))
            sona.species = table_data.get('species')
            sona.bio = table_data.get('bio')
            sona.image = table_data.get('image')
            sona.color = int(table_data.get('color'))
            sona.likes = table_data.get('likes')
            sona.verified = False
            async with self.bot.database() as db:
                await sona.save(db)


            if table_data['nsfw'] == True:
                embed = utils.ProfileEmbed(user=ctx.author, type="Nsfw_Sona", staff=True)
            else:
                embed = utils.ProfileEmbed(user=ctx.author, type="Sfw_Sona", staff=True)
            msg = await self.mail_box.send(f"{author.mention}'s Sona:", embed=embed)
            await msg.add_reaction('✅')
            await msg.add_reaction('🔴')

            embed2=Embed(description="**Your sona has been sent and must be first accepted by staff!**")
            await author.send(embed=embed2)

        except DiscordException:
            await author.send('I\'m unable to DM you?')

        except SonaCancelled:
            await author.send('Aborting Sona Creation!')

        except TimeoutError:
            await author.send('Sorry, but you took too long to respond.  Verification has closed.')
        
        except Exception as e:
            await author.send(f'An Error Occured: `{e}` Don\'t worry dev was notified!')
            await self.bot_log.send(embed=utils.LogEmbed(type="negative", title=f"Sona Creation Error", desc=f"Error: `{e}`"))
            raise e



def setup(bot):
    x = Sonas(bot)
    bot.add_cog(x)