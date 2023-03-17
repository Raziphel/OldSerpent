import typing
from dataclasses import dataclass, field

import discord


@dataclass
class StarredMessage:
    user_id: int
    reference_channel_id: int
    reference_message_id: int
    jump_link: str
    message_id: typing.Optional[int] = None
    star_count: int = 1
    attachment_messages: list[int] = field(default_factory=list)


class Starboards:
    starred_messages: typing.Dict[int, StarredMessage]

    def __init__(self, database):
        self.starred_messages = dict()
        self.database = database

    def cache(self, **starred_message_data):
        starred_message = StarredMessage(**starred_message_data)
        self.starred_messages[starred_message.reference_message_id] = starred_message

    async def add_to_starboard(
            self,
            reference_message_id: int,
            starboard_message_id: int,
            attachment_message_ids: list[int]
    ):
        async with self.database() as database:
            await database(
                'UPDATE starboard SET message_id = $1, attachment_messages = $2::bigint[] '
                'WHERE reference_message_id = $3',
                starboard_message_id, attachment_message_ids, reference_message_id
            )

    async def delete(self, message_id: int):
        async with self.database() as database:
            await database(
                'DELETE FROM starboard WHERE reference_message_id = $1',
                message_id
            )

            del self.starred_messages[message_id]

    async def decr(self, message_id: int) -> StarredMessage:
        async with self.database() as database:
            await database(
                'UPDATE starboard SET star_count = star_count - 1 '
                'WHERE reference_message_id = $1',
                message_id
            )

            starred_message = self.starred_messages[message_id]
            starred_message.star_count -= 1

            return starred_message

    async def incr(self, message_id: int) -> StarredMessage:
        async with self.database() as database:
            await database(
                'UPDATE starboard SET star_count = star_count + 1 '
                'WHERE reference_message_id = $1',
                message_id
            )

            starred_message = self.starred_messages[message_id]
            starred_message.star_count += 1

            return starred_message

    async def insert(self, starred_message: StarredMessage):
        async with self.database() as database:
            await database(
                'INSERT INTO starboard '
                '(user_id, message_id, reference_channel_id, '
                'reference_message_id, jump_link, star_count, '
                'attachment_messages) '
                'VALUES ($1, $2, $3, $4, $5, $6, $7::bigint[])',
                starred_message.user_id, starred_message.message_id, starred_message.reference_channel_id,
                starred_message.reference_message_id, starred_message.jump_link, starred_message.star_count,
                starred_message.attachment_messages
            )

            self.starred_messages[starred_message.reference_message_id] = starred_message

    def get_total_stars(self, user: typing.Union[discord.User, discord.Member]):
        return sum(
            starred_message.star_count for starred_message in self.starred_messages.values()
            if starred_message.user_id == user.id
        )
