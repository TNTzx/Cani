import discord
from discord import guild
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


class Cooldown:
    length = 0
    typeOfCooldown = cmds.BucketType.channel

class Require:
    def __init__(self):
        self.guildOwner = False
        self.guildAdmin = False
        self.dev = False

class Helps:
    def __init__(self):
        self.category = ""
        self.description = ""
        self.parameters = {}
        self.aliases = []
        self.guildOnly = True
        self.cooldown = Cooldown()
        self.require = Require()
        self.showCondition = lambda ctx: True
        self.exampleUsage = []
    
class CustomCommandClass:
    def __init__(self):
        self.name = ""
        self.help = Helps()

class ListOfCommands:
    commandsAll = {}
    commands = {}


for attribute in dir(Categories):
    if not attribute.startswith("__"):
        ListOfCommands.commandsAll[getattr(Categories, attribute)] = []


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
                    adminRole = fi.getData(['guilds', str(ctx.guild.id), 'mainData', 'adminRole'])
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
        

        cmd = CustomCommandClass()
        
        cmd.name = func.__name__
        help = cmd.help

        help.category = category
        help.description = description
        help.parameters = parameters
        help.aliases = aliases
        help.cooldown.length = cooldown
        help.cooldown.typeOfCooldown = cooldownType
        help.guildOnly = guildOnly

        require = help.require
        require.dev = requireDev
        require.guildAdmin = requireGuildAdmin
        require.guildOwner = requireGuildOwner
        help.require = require

        help.showCondition = showCondition
        help.exampleUsage = exampleUsage

        cmd.help = help

        if not cmd.name in ListOfCommands.commandsAll[category]:
            ListOfCommands.commandsAll[category].append(cmd.name)

        if not cmd.name in ListOfCommands.commands.keys():
            ListOfCommands.commands[cmd.name] = cmd
        for alias in aliases:
            if not alias in ListOfCommands.commands.keys():
                ListOfCommands.commands[alias] = cmd
        return wrapper

    return decorator

