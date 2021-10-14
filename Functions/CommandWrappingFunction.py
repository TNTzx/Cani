import discord
import discord.ext.commands as cmds
import functools as fc

from GlobalVariables import variables as varss
from Functions import FirebaseInteraction as fi
from Functions import CustomExceptions as ce
from Functions import ExtraFunctions as ef

class Categories:
    channelClaiming = "Channel Claiming"
    basicCommands = "Basic Commands"
    barking = "Barking"
    fun = "Fun"
    moderation = "Moderation"
    botControl = "Bot Control"
    
helpData = {}

for attribute in dir(Categories):
    if not attribute.startswith("__"):
        helpData[getattr(Categories, attribute)] = {}


def command(
        category=Categories.basicCommands,
        description="TNTz forgot to put a description lmao please ping him",
        parameters={},
        aliases=[],
        guildOnly=True,
        cooldown=0, cooldownType="",

        requireGuildOwner=False,
        requireGuildAdmin=False,
        requireDev=False,

        showCondition=lambda ctx: True,
        exampleUsage=[]
        ):
    
    def decorator(func):
        @fc.wraps(func)
        async def wrapper(*args, **kwargs):
            self = args[0]
            ctx: cmds.Context = args[1]

            devs = fi.getData(['mainData', 'devs'])

            async def sendError(suffix):
                await ef.sendError(ctx, f"*You don't have proper permissions!* {suffix}")
                return


            async def checkAdmin():
                    try:
                        adminRole = fi.getData(['guilds', ctx.guild.id, 'mainData', 'adminRole'])
                        adminRole = int(adminRole)
                    except ce.FirebaseNoEntry:
                        return False

                    for role in ctx.author.roles:
                        if role.id == adminRole:
                            return True
                    return False
            
            async def checkOwner():
                return ctx.author.id == ctx.guild.owner.id
            
            async def checkDev():
                return str(ctx.author.id) in devs


            if requireDev:
                if not await checkDev():
                    await sendError("*Only developers of this bot may do this command! >:(*")
                    return

            if requireGuildOwner:
                if not await checkOwner():
                    await sendError("*Only the server owner can do this command! >:(*")
                    return
            
            if requireGuildAdmin:
                if not (await checkAdmin() or await checkOwner()):
                    await sendError("*Only admins of this server may do this command! >:(*")
                    return

            if not showCondition(ctx):
                ctx.command.reset_cooldown(ctx)
                return
            return await func(*args, **kwargs)

        wrapper = cmds.command(name=func.__name__, aliases=aliases)(wrapper)

        if guildOnly:
            wrapper = cmds.guild_only()(wrapper)

        if cooldown > 0:
            wrapper = cmds.cooldown(1, cooldown, cooldownType)(wrapper)


        cdTypeGotten = cooldownType
        if cdTypeGotten == cmds.BucketType.user:
            cdTypeGot = "User"
        elif cdTypeGotten == cmds.BucketType.guild:
            cdTypeGot = "Entire Server"
        else:
            cdTypeGot = "Not Defined"


        cmdData = {
            "description": description,
            "parameters": parameters,
            "aliases": aliases,
            "guildOnly": guildOnly,
            "cooldown": {
                "length": cooldown,
                "type": cdTypeGot
            },
            "requireAdmin": requireGuildAdmin,
            "showCondition": showCondition,
            "exampleUsage": exampleUsage
        }
        helpData[category][func.__name__] = cmdData


        return wrapper

    return decorator

