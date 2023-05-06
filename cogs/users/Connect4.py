import asyncio
import logging
import typing
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord.ext.commands import command, Cog, ApplicationCommandMeta

import utils


VALID_EMOJI = ['{}️⃣'.format(number) for number in range(1, 8)]


class ConnectFourGame():
    NEUTRAL_CHIP = '⚪'
    PLAYER_ONE_CHIP = '🔴'
    PLAYER_TWO_CHIP = '🟡'

    CHECK_DELTAS = ((1, 0), (0, 1), (1, 1), (1, -1))
    DELTA_MULTIPLIERS = (1, -1)

    __slots__ = ('player_one', 'player_two', 'bet', 'current_player', 'board', 'expiration')

    def __init__(self, player_one: discord.Member, player_two: discord.Member, bet: typing.Optional[int] = None):
        self.player_one = player_one
        self.player_two = player_two
        self.bet = bet

        self.current_player = 1
        self.board = [[0 for _ in range(7)] for _ in range(6)]

        self.expiration = datetime.utcnow() + timedelta(minutes=8)

    def make_move(self, row, column):
        self.board[row][column] = self.current_player

    def next_available_row(self, column):
        return next(row for row in range(0, 6) if self.board[row][column] == 0)

    @property
    def visual_state(self):
        column_headers = ' '.join(VALID_EMOJI)
        board = self.draw_board()

        player_one = f'\n{self.PLAYER_ONE_CHIP} {self.player_one.mention} - ' \
                     f'**{"Now" if self.current_player == 1 else "Next"}**'
        player_two = f'{self.PLAYER_TWO_CHIP} {self.player_two.mention} - ' \
                     f'**{"Now" if self.current_player == 2 else "Next"}**'

        return '\n'.join((column_headers, board, player_one, player_two))

    def draw_board(self):
        # Replace 0, 1 and 2 with circle emojis and flip the board upside-down.
        def transform(row):
            def replace_chip(chip):
                if chip == 1:
                    return self.PLAYER_ONE_CHIP
                elif chip == 2:
                    return self.PLAYER_TWO_CHIP
                else:
                    return self.NEUTRAL_CHIP

            return [replace_chip(chip) for chip in row]

        transformed_board = [transform(row) for row in self.board]
        upside_down_board = reversed(transformed_board)

        board = '\n'.join(' '.join(row) for row in upside_down_board)

        return board

    def is_position_win(self, row, column):
        search_value = self.board[row][column]

        for delta_move in self.CHECK_DELTAS:
            delta_row, delta_column = delta_move
            streak = 1

            for delta in self.DELTA_MULTIPLIERS:
                delta_row *= delta
                delta_column *= delta
                next_row = row + delta_row
                next_column = column + delta_column

                while 0 <= next_row < 6 and 0 <= next_column < 7:
                    if self.board[next_row][next_column] == search_value:
                        streak += 1
                    else:
                        break
                    if streak == 4:
                        return True

                    next_row += delta_row
                    next_column += delta_column

        return False

    def is_board_full(self):
        return not any(not column for column in self.board[-1])


class ConnectFour(Cog):
    MAX_DAILY_BET_TOTAL = 2500  # User can't wager this much against another person in a day.
    MAX_BET_PER_GAME = 1500  # User can't bet more than this per game.
    ENCLOSING_KEYCAP = '️⃣'
    CHANNEL_ID = 702993838066630727  # Connect-4 Furry Royale channel

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('four')
        self.logger.setLevel(level=logging.DEBUG)

        self.games = {}
        self.users = {}
        self.pending = set()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(f"{ctx.author.mention} I couldn't get the user you mentioned.", delete_after=15)

    async def finish_game(self, message: discord.Message):
        game = self.games[message.id]

        try:
            del self.users[game.player_one.id]
            del self.users[game.player_two.id]
            del self.games[message.id]
            await message.clear_reactions()
        except KeyError as err:
            self.logger.debug(f'There was an error finishing a game: {err}')
        except discord.DiscordException as err:
            self.logger.debug(f'There was an error clearing game reaction: {err}')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, member: discord.Member):
        """Handles the user dropping a chip in a specific column."""
        if member.bot:
            return

        if reaction.message.id not in self.games:
            return

        emoji = str(reaction.emoji)
        channel = self.bot.get_channel(reaction.message.channel.id)
        message = await channel.fetch_message(reaction.message.id)

        if str(reaction.emoji) not in VALID_EMOJI:
            return await message.remove_reaction(emoji, member)

        # self.logger.debug(f'Got emoji: {emoji}')

        game = self.games[reaction.message.id]

        if (game.current_player == 1 and game.player_one.id != member.id) or \
                (game.current_player == 2 and game.player_two.id != member.id):
            return await message.remove_reaction(emoji, member)

        stripped_number = emoji.replace(self.ENCLOSING_KEYCAP, str())
        column = int(stripped_number) - 1

        try:
            row = game.next_available_row(column)
        except StopIteration:
            return  # Invalid move. That column is full.

        # self.logger.debug(f'User is trying to place in column {column} row {row}')

        game.make_move(row, column)

        if game.is_position_win(row, column):
            await self.finish_game(message)
            if game.bet:
                async with self.bot.database() as database:
                    user_crowns = UserCrowns.get(member.id)
                    user_crowns.crowns += game.bet * 2
                    await user_crowns.save(database)

                    coin_e = self.bot.config['emotes']['coin']
                    await message.channel.send(f'{member.mention} wins and earns {game.bet:,} {coin_e}!')

                    self.logger.debug(f'Gave coins to {member} for winning.')
            else:
                await message.channel.send(f'{member.mention} wins!')

        elif game.is_board_full():
            await self.finish_game(message)
            if game.bet:
                async with self.bot.database() as database:
                    user_crowns = UserCrowns.get(member.id)
                    opponent_crowns = UserCrowns.get(game.player_one.id if game.current_player == 1 else
                                                     game.player_two.id)
                    user_crowns.crowns += game.bet
                    opponent_crowns.crowns += game.bet

                    await user_crowns.save(database)
                    await opponent_crowns.save(database)

                    await message.channel.send("It's a tie! Both players have had their coins returned to them.")

                    self.logger.debug(f'Returned money to {member} and their opponent.')
            else:
                await message.channel.send("It's a tie!")
        else:
            await message.remove_reaction(emoji, member)
            game.current_player = 2 if game.current_player == 1 else 1

        board = game.visual_state
        await message.edit(content=board)

    @command(aliases=['connect4', 'c4'])
    async def connectfour(self, ctx: commands.Context, member: discord.Member, amount: typing.Optional[int] = None):
        """Challenge another member to a game of connect four with an optional bet."""
        if ctx.channel.id in (self.bot.config['channels']['general'],
                              self.bot.config['channels']['adult_general']):
            return await ctx.send(f'You cannot play Connect 4 in this channel.')
        if ctx.author.id == member.id:
            return await ctx.send(f"{ctx.author.mention} you can't play against yourself.", delete_after=15)
        if ctx.author.id in self.pending:
            return await ctx.send(f'{ctx.author.mention} you currently have a pending Connect 4 request.',
                                  delete_after=15)
        if member.id in self.pending:
            return await ctx.send(f'{ctx.author.mention} that person already has a pending Connect 4 request.',
                                  delete_after=15)
        if ctx.author.id in self.users:
            message = self.users[ctx.author.id]
            game = self.games[message]
            if game.expiration > datetime.utcnow():
                return await ctx.send(f"{ctx.author.mention} you must finish your current game before starting a new "
                                      f"one.", delete_after=15)
            try:
                del self.users[ctx.author.id]
                del self.users[member.id]
                del self.games[message]
            except KeyError as err:
                self.logger.debug(f'Error deleting game keys: {err}')

        if member.id in self.users:
            return await ctx.send(f'{ctx.author.mention} that person is currently in a game.', delete_after=15)

        # We define them here even if we don't need them to avoid stupid PyCharm warnings.
        u_c = utils.Currency.get(ctx.author.id)
        o_c = utils.Currency.get(member.id)

        if amount is not None:
            if amount < 0 or amount > self.MAX_BET_PER_GAME:
                return await ctx.send(f'The amount of crowns you bet must be between 0 and '
                                      f'{self.MAX_BET_PER_GAME:,}')

            if amount > u_c.crowns or amount > o_c.crowns:
                return await ctx.send(f"{ctx.author.mention} you can't bet more than what you or your opponent have.",
                                      delete_after=15)

            question = await ctx.send(f':video_game: {member.mention} {ctx.author.mention} would like to challenge you '
                                      f'to a game of Connect 4 with **{amount:,}** :crown: on the line, what say you?', )
        else:
            question = await ctx.send(f':video_game: {member.mention} {ctx.author.mention} would like to challenge you '
                                      f'to a game of Connect 4, what do you say?')

        self.pending.add(ctx.author.id)
        self.pending.add(member.id)

        question_emojis = ('👍', '👎')

        for emoji in question_emojis:
            await question.add_reaction(emoji)

        def check(r: discord.Reaction, u: discord.User):
            return r.message.id == question.id and u.id == member.id and str(r.emoji) in question_emojis

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=45.0)

            self.pending.remove(ctx.author.id)
            self.pending.remove(member.id)

            if str(reaction.emoji) == '👎':
                await question.delete()
                return await ctx.send(f"{ctx.author.mention} Seems like {member.mention} isn't interested in playing. "
                                      f":(")
        except asyncio.TimeoutError:
            self.pending.remove(ctx.author.id)
            self.pending.remove(member.id)

            return await ctx.send(f'{ctx.author.mention} they took too long to respond to your challenge. Sowwy.')

        if amount is not None:
            u_c.coins -= amount
            o_c.coins -= amount
            async with self.bot.database() as database:
                await u_c.save(database)
                await o_c.save(database)

        await question.delete()

        game = ConnectFourGame(ctx.author, member, amount)
        board = game.visual_state

        message = await ctx.send(board)

        for emoji in VALID_EMOJI:
            await message.add_reaction(emoji)

        self.games[message.id] = game
        self.users[ctx.author.id] = message.id
        self.users[member.id] = message.id


def setup(bot):
    bot.add_cog(ConnectFour(bot))
