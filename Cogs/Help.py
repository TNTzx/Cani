import discord
import discord.ext.commands as cmds

import main

from Functions import ExtraFunctions as ef
from Functions import CustomExceptions as ce
from Functions import CommandWrapper as cw


color = 0x7289da


class Help(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot
        main.bot.remove_command("help")


    def getCommand(self, ctx, command):
        for category, commands in cw.helpData.items():
            if command in commands:
                return cw.helpData[category][command], category
        return None, None

    async def create_help(ctx, commandName, category, description,
            parameters={},
            aliases=[],
            guildOnly=True,
            requireAdmin=False,
            cooldown=0,
            exampleUsage=[]):

        embed = discord.Embed(name="Help", title=f"{category}: {main.commandPrefix}{commandName}", color=color)
        embed.add_field(name=f"Description", value=description)
        embed.add_field(name="`~~                                     ~~`", value="_ _", inline=False)

        if not len(parameters) == 0:
            paramsSyntax = "> <".join([x for x in parameters.keys()])
            embed.add_field(name=f"Syntax:", value=f"`{main.commandPrefix}{commandName} <{paramsSyntax}>`", inline=False)
            
            paramsList = "\n".join([f"`<{params}>`: {paramsDesc}" for params, paramsDesc in parameters.items()])
            embed.add_field(name=f"Parameters:", value=f"{paramsList}", inline=False)

        if not len(aliases) == 0:
            aliasNames = "`, `".join(aliases)
            embed.add_field(name=f"Aliases:", value=f"`{aliasNames}`", inline=False)

        embed.add_field(name="`~~                                     ~~`", value="_ _", inline=False)

        if guildOnly:
            embed.add_field(name=f"Guild Only:", value=f"`Yes`")
        else:
            embed.add_field(name=f"Guild Only:", value=f"`No`")

        if requireAdmin:
            embed.add_field(name=f"Required role:", value=f"`{main.adminRole}`")

        if not cooldown["length"] == 0:
            cooldownForm = await ef.formatTime(cooldown["length"])
            cooldownType = cooldown["type"]
            embed.add_field(name=f"Cooldown:", value=f"`Length: {cooldownForm}\nApplies to: {cooldownType}`")
        
        if not len(exampleUsage) == 0:
            exUseform = "`\n`".join(exampleUsage)
            embed.add_field(name=f"Example:", value=f"`{exUseform}`", inline=False)

        return embed
    

    @main.bot.group(invoke_without_command=True, aliases=["h"])
    async def help(self, ctx, *args):
        await ctx.send("*Getting help...*")

        async def showCondition(ctx, category, command):
            return cw.helpData[category][command]["showCondition"](ctx)

        if not len(args) == 0:
            command = args[0]
            cmdDict, category = self.getCommand(ctx, command)

            async def notFoundError():
                await ef.sendError(ctx, "*Documentation for command not found! Make sure you used the actual name instead of the alias and check your spelling!*")
                raise ce.ExitFunction("Exited Function.")

            if cmdDict == None or (not await showCondition(ctx, category, command)):
                await notFoundError()

            embed = await Help.create_help(ctx, command, category,
                cmdDict["description"],
                parameters = cmdDict["parameters"],
                aliases = cmdDict["aliases"],
                guildOnly = cmdDict["guildOnly"],
                cooldown = cmdDict["cooldown"],
                requireAdmin = cmdDict["requireAdmin"],
                exampleUsage = cmdDict["exampleUsage"]
            )
        else:
            embed = discord.Embed(name="Help", title="Help!", description=f"what the dog doin\n__Command Prefix:__ **{main.commandPrefix}**", color=color)
            embed.set_footer(text=f"Type {main.commandPrefix}help <command> for more information to a command.")

            for category, commands in cw.helpData.items():
                cmdList = commands.keys()
                cmdAllowed = [command for command in cmdList if await showCondition(ctx, category, command)]
                commandFormat = f"`{'`, `'.join(cmdAllowed)}`"
                embed.add_field(name=category, value=commandFormat, inline=False)

        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Help(bot))