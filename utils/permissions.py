from discord import DMChannel

from discord.ext.commands import has_any_role, check, CommandError, has_permissions






#! Built in permissions
def is_in_dms():
    '''Commands only runnable in dms'''
    async def predicate(ctx):
        if ctx.message.guild != None:
            raise InDmsCheckError()
        return True
    return check(predicate)

def is_user(*user_ids):
    '''Commands only certain id's can run'''
    async def predicate(ctx):
        if ctx.author.id in ctx.bot.developers:
            return True
        if ctx.author.id not in user_ids:
            raise UserCheckError
        return True
    return check(predicate)

def is_dev():
    '''Commands only the bot dev can run'''
    async def predicate(ctx):
        if ctx.author.id not in ctx.bot.developers:
            raise DevCheckError()
        return True
    return check(predicate)





#! Guild specific permissions 
def is_guild(*guild_ids):
    '''Commands only made for the realm'''
    async def predicate(ctx):
        if ctx.guild.id not in guild_ids:
            raise GuildCheckError
        return True
    return check(predicate)





#! Main used permissions
def is_nsfw():
    '''Commands only made for NSFW channels.'''
    def predicate(ctx):
        if ctx.author.id in ctx.bot.developers:
            return True
        if isinstance(ctx.channel, DMChannel) or not ctx.channel.nsfw:
            raise NSFWCheckError()
        return True
    return check(predicate)


def is_nsfw_staff():
    '''Commands only made for NSFW mods. Only works in nsfw channels.'''
    def predicate(ctx):
        if ctx.author.id in ctx.bot.developers:
            return True
        if [i for i in ctx.author.roles if i.id in ctx.bot.nsfw_staff]:
            return True
        raise NSFWStaffCheckError
    return check(predicate)


def is_mod_staff():
    '''Commands only made for mods'''
    def predicate(ctx):
        if ctx.author.id in ctx.bot.developers:
            return True
        if [i for i in ctx.author.roles if i.id in ctx.bot.mod_staff]:
            return True
        raise ModStaffCheckError
    return check(predicate)


def is_admin_staff():
    '''Commands only made for admins'''
    def predicate(ctx):
        if ctx.author.id in ctx.bot.developers:
            return True
        if [i for i in ctx.author.roles if i.id in ctx.bot.admin_staff]:
            return True
        raise AdminStaffCheckError
    return check(predicate)


def is_owner_staff():
    '''Commands only made for owners'''
    def predicate(ctx):
        if ctx.author.id in ctx.bot.developers:
            return True
        if [i for i in ctx.author.roles if i.id in ctx.bot.owner_staff]:
            return True
        raise OwnerStaffCheckError
    return check(predicate)





#! Built In Permissions
class InDmsCheckError(CommandError):
    pass
class UserCheckError(CommandError):
    pass
class DevCheckError(CommandError):
    pass

#! Guild Permissions
class GuildCheckError(CommandError):
    pass


#! Main Staff Permisions
class NSFWCheckError(CommandError):
    pass
class NSFWStaffCheckError(CommandError):
    pass
class ModStaffCheckError(CommandError):
    pass
class AdminStaffCheckError(CommandError):
    pass
class OnwerStaffCheckError(CommandError):
    pass

