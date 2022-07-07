# Discord
from discord.ext.commands import command, cooldown, BucketType, Cog
from discord import Member, Message, User, TextChannel, guild, channel

import utils

from asyncio import sleep
from random import randint, choice
from math import floor

class ChannelFunction(object):
    bot = None

    @classmethod
    async def get_log_channel(cls, guild, log:str):
        '''Gets the correct log channel, from the correct guild'''

        #! The realms logs
        if guild.id == cls.bot.config['guilds']['RaziRealmID']:
            if log == "bot":
                return cls.bot.get_channel(cls.bot.config['channels']['realm']['log']['bot_log'])
            elif log == "currency":
                return cls.bot.get_channel(cls.bot.config['channels']['realm']['log']['currency_log'])
            elif log == "member":
                return cls.bot.get_channel(cls.bot.config['channels']['realm']['log']['member_log'])
            elif log == "message":
                return cls.bot.get_channel(cls.bot.config['channels']['realm']['log']['message_log'])
            elif log == "welcome":
                return cls.bot.get_channel(cls.bot.config['channels']['realm']['welcome'])
            elif log == "sfw_mail":
                return cls.bot.get_channel(cls.bot.config['channels']['realm']['sfw_mail'])
            elif log == "sfw_archive":
                return cls.bot.get_channel(cls.bot.config['channels']['realm']['sfw_archive'])

        elif guild.id == cls.bot.config['guilds']['FurryRoyaleID']:
            if log == "bot":
                return cls.bot.get_channel(cls.bot.config['channels']['royale']['log']['bot_log'])
            elif log == "currency":
                return cls.bot.get_channel(cls.bot.config['channels']['royale']['log']['currency_log'])
            elif log == "member":
                return cls.bot.get_channel(cls.bot.config['channels']['royale']['log']['member_log'])
            elif log == "message":
                return cls.bot.get_channel(cls.bot.config['channels']['royale']['log']['message_log'])
            elif log == "welcome":
                return cls.bot.get_channel(cls.bot.config['channels']['royale']['welcome'])
            elif log == "sfw_mail":
                return cls.bot.get_channel(cls.bot.config['channels']['royale']['sfw_mail'])
            elif log == "sfw_archive":
                return cls.bot.get_channel(cls.bot.config['channels']['royale']['sfw_archive'])
            elif log == "sonas":
                return cls.bot.get_channel(cls.bot.config['channels']['royale']['sonas'])