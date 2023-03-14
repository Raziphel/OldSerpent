from re import compile as _compile

from discord.ext.commands import BadArgument, Converter


class TimeConverter(Converter):

    def __init__(self):
        self.matcher = _compile(r'((\d+)d)?((\d+)h)?((\d+)m)?((\d+)s)?')

    async def convert(self, ctx, arg: str) -> int:
        '''Converts the argument to an integer based on the amount of time given'''

        # No number type specified
        if arg.isdigit():
            return int(arg)

        # Regex it up
        matches = self.matcher.match(arg)
        if not matches.group(0):
            raise BadArgument()

        # Convert times etc
        total = 0
        if matches.group(2):
            # days
            total += int(matches.group(2)) * 60 * 60 * 24
        if matches.group(4):
            # hours
            total += int(matches.group(4)) * 60 * 60
        if matches.group(6):
            # minutes
            total += int(matches.group(6)) * 60
        if matches.group(8):
            # seconds
            total += int(matches.group(8))

        if total == 0:
            raise BadArgument()

        return total
