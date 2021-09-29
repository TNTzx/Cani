import discord
from discord.ext import commands

import main
from Functions import extraFunctions as eF
from Functions import firebaseInteraction as fi
from Cogs import ChannelClaiming as cc
from Functions import HelpData as hd

color = 0x7289da


class Help(commands.Cog):
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
            paramsKeyList = parameters.keys()

            paramsKeyListForm = []
            for params in paramsKeyList:
                paramsKeyListForm.append(f"<{params}>")
            
            paramsKeyListFormSpace = " ".join(paramsKeyListForm)
            embed.add_field(name=f"Syntax:", value=f"`{main.commandPrefix}{commandName} {paramsKeyListFormSpace}`", inline=False)
            
            paramsList = []
            for params, paramsDesc in parameters.items():
                paramsList.append(f"`<{params}>`: {paramsDesc}")

            paramsListForm = "\n".join(paramsList)
            embed.add_field(name=f"Parameters:", value=f"{paramsListForm}", inline=False)

        if not cooldown == 0:
            cooldownForm = await eF.formatTime(cooldown)
            embed.add_field(name=f"Cooldown:", value=f"`{cooldownForm}`", inline=False)
        
        if not len(exampleUsage) == 0:
            exUseForm = "`\n`".join(exampleUsage)
            embed.add_field(name=f"Example:", value=f"`{exUseForm}`", inline=False)

        await ctx.send(embed=embed)
    

    @main.bot.group(invoke_without_command=True, aliases=["h"])
    async def help(self, ctx, *args):
        if not len(args) == 0:
            command = args[0]
            cmdDict, category = self.getCommand(ctx, command)

            showCondition = hd.helpData(ctx)[category][command].get("showCondition", lambda: True)
            if cmdDict == None or (not showCondition()):
                await eF.sendError(ctx, "*Documentation for command not found! Are you sure you typed it correctly?*")
                return

            await Help.create_help(ctx, command, category, cmdDict["description"],
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
                cmdAllowed = []
                for command in cmdList:
                    showCondition = hd.helpData(ctx)[category][command].get("showCondition", lambda: True)
                    if showCondition():
                        cmdAllowed.append(command)
                        continue

                commandFormat = f"`{'`, `'.join(cmdAllowed)}`"
                embed.add_field(name=category, value=commandFormat, inline=False)

            await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Help(bot))