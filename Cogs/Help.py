import discord
import discord.ext.commands as cmds

import main

from Functions import ExtraFunctions as ef
from Functions import CustomExceptions as ce
from Functions import FirebaseInteraction as fi
from Cogs import ChannelClaiming as cc
from Functions import HelpData as hd


color = 0x7289da


class Help(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot
        main.bot.remove_command("help")


    def getCommand(self, ctx, command):
        for category, commands in hd.helpData(ctx).items():
            if command in commands:
                return hd.helpData(ctx)[category][command], category
        return None, None


    async def create_help(ctx, commandName, category, description, aliases=[], parameters={}, requireAdminRole=False, cooldown=0, exampleUsage=[]):
        embed = discord.Embed(name="Help", title=f"{category}: {main.commandPrefix}{commandName}", color=color)
        embed.add_field(name=f"Description", value=description)

        if not len(aliases) == 0:
            aliasNames = "`, `".join(aliases)
            embed.add_field(name=f"Aliases:", value=f"`{aliasNames}`", inline=False)

        if requireAdminRole:
            embed.add_field(name=f"Required role:", value=f"`{main.adminRole}`", inline=False)

        if not len(parameters) == 0:
            paramsSyntax = "> <".join([x for x in parameters.keys()])
            embed.add_field(name=f"Syntax:", value=f"`{main.commandPrefix}{commandName} <{paramsSyntax}>`", inline=False)
            
            paramsList = "\n".join([f"`<{params}>`: {paramsDesc}" for params, paramsDesc in parameters.items()])
            embed.add_field(name=f"Parameters:", value=f"{paramsList}", inline=False)

        if not cooldown == 0:
            cooldownForm = await ef.formatTime(cooldown)
            embed.add_field(name=f"Cooldown:", value=f"`{cooldownForm}`", inline=False)
        
        if not len(exampleUsage) == 0:
            exUseform = "`\n`".join(exampleUsage)
            embed.add_field(name=f"Example:", value=f"`{exUseform}`", inline=False)

        return embed
    

    @main.bot.group(invoke_without_command=True, aliases=["h"])
    async def help(self, ctx, *args):
        await ctx.send("*Getting help...*")

        async def showCondition(ctx, category, command):
            return hd.helpData(ctx)[category][command].get("showCondition", lambda: True)()

        if not len(args) == 0:
            command = args[0]
            cmdDict, category = self.getCommand(ctx, command)

            async def notFoundError():
                await ef.sendError(ctx, "*Documentation for command not found! Make sure you used the actual name instead of the alias and check your spelling!*")
                raise ce.ExitFunction("Exited Function.")

            if cmdDict == None or (not await showCondition(ctx, category, command)): await notFoundError()

            embed = await Help.create_help(ctx, command, category, cmdDict["description"],
                aliases = cmdDict.get("aliases", []),
                parameters = cmdDict.get("parameters", {}),
                requireAdminRole = cmdDict.get("requireAdminRole", False),
                cooldown = cmdDict.get("cooldown", 0),
                exampleUsage = cmdDict.get("exampleUsage", [])
            )
        else:
            embed = discord.Embed(name="Help", title="Help!", description=f"what the dog doin\n__Command Prefix:__ **{main.commandPrefix}**", color=color)
            embed.set_footer(text=f"Type {main.commandPrefix}help <command> for more information to a command.")

            for category, commands in hd.helpData(ctx).items():
                cmdList = commands.keys()
                cmdAllowed = [command for command in cmdList if await showCondition(ctx, category, command)]
                commandFormat = f"`{'`, `'.join(cmdAllowed)}`"
                embed.add_field(name=category, value=commandFormat, inline=False)

        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Help(bot))