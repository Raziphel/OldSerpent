import discord
from discord.ext import commands

from serpent import Serpent
from utils.sql.users.starboard import Starboards, StarredMessage


# TODO: add button to list of components that shows the message the author was responding to

class StarboardHandler(commands.Cog):
    REGULAR_STARBOARD_THRESHOLD = 5
    SUGGESTION_STARBOARD_THRESHOLD = 14

    REGULAR_GLOWING_STAR_THRESHOLD = 15
    SUGGESTION_GLOWING_STAR_THRESHOLD = 20

    STAR_EMOJI = '\N{White Medium Star}'
    GLOWING_STAR_EMOJI = '\N{Glowing Star}'
    ADULT_CHANNEL_EMOJI = '\N{Beer Mug}'
    CUSTOM_UPVOTE_EMOJI = '<:UpVote:1041606985080119377>'

    def __init__(self, bot: Serpent):
        self.bot = bot
        self.starboards = Starboards(self.bot.database)

        self.bot.loop.create_task(self.starboard_preparation())

    async def starboard_preparation(self):
        await self.bot.wait_until_ready()

        async with self.bot.database() as database:
            starboard = await database('SELECT * FROM starboard')

            for starred_message in starboard:
                self.starboards.cache(**starred_message)

            print(f'[debug] loaded {len(starboard)} starred messages into cache')

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        return  # Currently disabled and untested.
        if payload.message_id in self.starboards.starred_messages:
            # A starred messages was deleted.
            starred_message = self.starboards.starred_messages[payload.message_id]

            # Delete message from starboard
            guild = self.bot.get_guild(payload.guild_id)
            starboard_channel = guild.get_channel(self.bot.config['channels']['starboard'])

            try:
                starboard_message = await starboard_channel.fetch_message(starred_message.message_id)
                await starboard_message.delete()
            except discord.DiscordException as err:
                print(f'[error] unable to delete starboard message. message id: {starred_message.message_id} - {err}')

            for attachment_message_id in starred_message.attachment_messages:
                try:
                    attachment_message = await starboard_channel.fetch_message(attachment_message_id)
                    await attachment_message.delete()
                except discord.DiscordException as err:
                    print(
                        f'[error] unable to delete starboard attachment message. '
                        f'message id: {attachment_message_id} - {err}'
                    )

            await self.starboards.delete(starred_message.reference_message_id)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if not payload.guild_id:
            return  # Ignore DMs

        if str(payload.emoji) in (self.STAR_EMOJI, self.CUSTOM_UPVOTE_EMOJI):
            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)

            if str(payload.emoji) == self.STAR_EMOJI and channel.id in (
                    self.bot.config['channels']['suggestions'],
                    self.bot.config['channels']['premium_suggestions']
            ):
                return  # Cannot use star emoji in suggestion channels

            try:
                if str(payload.emoji) == self.CUSTOM_UPVOTE_EMOJI and channel.id not in (
                        self.bot.config['channels']['suggestions'],
                        self.bot.config['channels']['premium_suggestions']
                ):
                    return  # Custom upvote emoji can only be used in suggestion channels
            except: pass

            message = await channel.fetch_message(payload.message_id)  # The original message
            starboard_channel = guild.get_channel(self.bot.config['channels']['starboard'])

            # Just in case, I guess?
            if message.id in self.starboards.starred_messages:
                starred_message = await self.starboards.decr(message.id)

                print(f'[debug] starred message new star count: {starred_message.star_count}')

                if starred_message.star_count <= 0:
                    # Time to remove the message from the starboard
                    try:
                        starboard_message = await starboard_channel.fetch_message(starred_message.message_id)
                        await starboard_message.delete()
                    except discord.DiscordException as err:
                        print(
                            f'[error] failed to delete starboard message (maybe it was already deleted?) '
                            f'message id: {starred_message.message_id} - {err}'
                        )

                    # Now delete any extra attachment messages
                    for attachment_message_id in starred_message.attachment_messages:
                        try:
                            attachment_message = await starboard_channel.fetch_message(attachment_message_id)
                            await attachment_message.delete()
                        except discord.DiscordException as err:
                            print(
                                f'[error] failed to delete extra starboard attachment message. '
                                f'message id: {attachment_message_id} - {err}'
                            )

                    # Remove from the database
                    return await self.starboards.delete(message.id)

                # Update the message with the new star count
                starboard_message = await starboard_channel.fetch_message(starred_message.message_id)
                star_emoji = self.GLOWING_STAR_EMOJI if starred_message.star_count >= 5 else self.STAR_EMOJI
                await starboard_message.edit(content=f'{star_emoji} {starred_message.star_count} | {channel.mention}')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if not payload.guild_id:
            return  # Ignore DMs

        if str(payload.emoji) in (self.STAR_EMOJI, self.CUSTOM_UPVOTE_EMOJI):
            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)

            if str(payload.emoji) == self.STAR_EMOJI and channel.id in (
                    self.bot.config['channels']['suggestions'],
                    self.bot.config['channels']['premium_suggestions']
            ):
                return  # Cannot use star emoji in suggestion channels

            if str(payload.emoji) == self.CUSTOM_UPVOTE_EMOJI and channel.id not in (
                    self.bot.config['channels']['suggestions'],
                    self.bot.config['channels']['premium_suggestions']
            ):
                return  # Custom upvote emoji can only be used in suggestion channels

            # Before doing anything else, make sure this isn't a message from the adult channels.
            if self.ADULT_CHANNEL_EMOJI in channel.name:
                return  # Exit

            # Person who reacted
            member = payload.member
            if member.bot:
                return  # Ignore bot reactions

            message = await channel.fetch_message(payload.message_id)

            member = message.author
            if member.bot:
                return  # Ignore bot messages

            starboard_channel = guild.get_channel(self.bot.config['channels']['starboard'])
            file_attachment_message = 'Please view the original message to see the attachment.'

            if message.id not in self.starboards.starred_messages:
                # Insert the information into the table
                starred_message = StarredMessage(
                    user_id=member.id,
                    message_id=None,
                    reference_channel_id=channel.id,
                    reference_message_id=message.id,
                    jump_link=message.jump_url,
                    star_count=1,
                    attachment_messages=[]
                )

                return await self.starboards.insert(starred_message)

            starred_message = await self.starboards.incr(message_id=message.id)
            starboard_threshold = self.REGULAR_STARBOARD_THRESHOLD if channel.id not in (
                self.bot.config['channels']['suggestions'],
                self.bot.config['channels']['premium_suggestions']
            ) else self.SUGGESTION_STARBOARD_THRESHOLD

            if starred_message.star_count == starboard_threshold:
                # Creating a new entry in the starboard channel
                embed = discord.Embed(
                    timestamp=message.created_at,
                    description=message.content,
                    colour=discord.Colour.gold()
                )
                embed.set_author(
                    name=str(member),
                    icon_url=member.avatar.url
                )
                embed.set_footer(text=f'Message ID: {message.id}')

                message_content = f'{self.STAR_EMOJI} {starboard_threshold} | {channel.mention}'

                components = discord.ui.MessageComponents(
                    discord.ui.ActionRow(
                        discord.ui.Button(
                            label="Original message",
                            style=discord.ui.ButtonStyle.link,
                            url=message.jump_url
                        ),
                    ),
                )

                attachment_message_ids = []

                if message.attachments:
                    # Treat the first message specially.
                    # We don't want to mutate the actual list, just in case.
                    attachments = message.attachments.copy()
                    attachment = attachments.pop()

                    if 'image' in attachment.content_type:
                        embed.set_image(url=attachment.url)
                    else:
                        embed.description = f'{message.content}\n\n**{file_attachment_message}**'

                    starboard_message = await starboard_channel.send(
                        content=message_content,
                        embed=embed,
                        components=components
                    )

                    for attachment in attachments:
                        # Send only the first attachment with timestamp and message ID information!
                        # Otherwise, reset information.

                        embed = discord.Embed(
                            colour=discord.Colour.gold()
                        )
                        # Since we're working with a new embed we need to set the author's information again.
                        embed.set_author(
                            name=str(member),
                            icon_url=member.avatar.url
                        )

                        if 'image' in attachment.content_type:
                            embed.set_image(url=attachment.url)
                        else:
                            embed.description = file_attachment_message

                        starboard_attachment_message = await starboard_channel.send(
                            embed=embed
                        )

                        attachment_message_ids.append(starboard_attachment_message.id)

                    return await self.starboards.add_to_starboard(
                        reference_message_id=message.id,
                        starboard_message_id=starboard_message.id,
                        attachment_message_ids=attachment_message_ids
                    )
                else:
                    starboard_message = await starboard_channel.send(
                        content=message_content,
                        embed=embed,
                        components=components
                    )

                    return await self.starboards.add_to_starboard(
                        reference_message_id=message.id,
                        starboard_message_id=starboard_message.id,
                        attachment_message_ids=attachment_message_ids
                    )

            elif starred_message.star_count > starboard_threshold:  # Update the counter
                try:
                    # get_partial_message might also work here, but I'm not sure how reliable it is.
                    starboard_message = await starboard_channel.fetch_message(starred_message.message_id)

                except discord.DiscordException as err:
                    return print(
                        f'[error] unable to retrieve starboard message. '
                        f'message id: {starred_message.message_id} - {err}'
                    )

                glowing_star_threshold = self.SUGGESTION_GLOWING_STAR_THRESHOLD if channel.id in (
                    self.bot.config['channels']['suggestions'],
                    self.bot.config['channels']['premium_suggestions']
                ) else self.REGULAR_GLOWING_STAR_THRESHOLD

                star_emoji = (
                    self.GLOWING_STAR_EMOJI if starred_message.star_count >= glowing_star_threshold
                    else self.STAR_EMOJI
                )

                return await starboard_message.edit(
                    content=f'{star_emoji} {starred_message.star_count} | {channel.mention}'
                )


def setup(bot: Serpent):
    bot.add_cog(StarboardHandler(bot))
