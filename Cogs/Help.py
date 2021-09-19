import discord
from discord.ext import commands

import main
from Functions import extraFunctions as eF
from Cogs import ChannelClaiming as cc

color = 0x7289da


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        main.bot.remove_command("help")

    helpDict = {
        "Channel Claiming": {
            "claimchannel": {
                "description": "Claims / unclaims the current RP channel to a specific location.",
                "parameters": {
                    "claim | unclaim": "Tells if you want to claim or unclaim the current RP channel.",
                    "location": "The location of where you want the channel to be in. Surround the location with quotes (example: `\"Imagination Room\"`)."
                },
                "aliases": [
                    "cc"
                ],
                "cooldown": cc.cooldownTime
            },
            # "unclaimchannel": {
            #     "description": "Unclaims the RP channel."
            # },
            "editclaimchannels":{
                "description": "Adds / removes the channel as an RP channel.",
                "parameters": {
                    "add | remove": "Tells if you want to add or remove a channel as an RP channel.",
                    "channel": "Channel that you want to add / remove as an RP channel."
                },
                "requireAdminRole": True,
                "aliases": [
                    "ecc"
                ]
            }
        },
        "Bot Control": {
            "killswitch": {
                "description": "Shuts the bot down.",
                "requireAdminRole": True
            },
            "restartswitch": {
                "description": "Restarts the bot.",
                "requireAdminRole": True
            }
        },
        "Fun": {
            "hello": {
                "description": "Sends a hello message! :D"
            },
            "ping": {
                "description": "I ping you back! :D"
            },
            "bark": {
                "description": "...why do you need help for a.. bark command..?"
            },
            "barkcount": {
                "description": "Displays how much I barked for this server!"
            }
        }
    }


    def getCommand(self, command):
        for category, commands in self.helpDict.items():
            if command in commands:
                return self.helpDict[category][command], category
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
    

    @main.bot.group(invoke_without_command=True)
    async def help(self, ctx, *args):
        if not len(args) == 0:
            command = args[0]
            cmdDict, category = self.getCommand(command)
            if cmdDict == None:
                await eF.sendError(ctx, "*Documentation for command not found! Are you sure you typed it correctly?*")
                return

            await Help.create_help(ctx, command, category, cmdDict["description"],
                aliases = cmdDict["aliases"],
                parameters = cmdDict.get("parameters", {}),
                requireAdminRole = cmdDict.get("requireAdminRole", False),
                cooldown = cmdDict.get("cooldown", 0),
                exampleUsage = cmdDict.get("exampleUsage", []))
        else:
            embed = discord.Embed(name="Help", title="Help!", description=f"what the dog doin\nCommand Prefix: {main.commandPrefix}", color=color)
            embed.set_footer(text=f"Type {main.commandPrefix}help <command> for more information to a command.")

            for category, commands in self.helpDict.items():
                commandFormat = f"`{'`, `'.join(commands.keys())}`"
                embed.add_field(name=category, value=commandFormat, inline=False)

            await ctx.send(embed=embed)

    

    # @help.command()
    # async def claimchannel(self, ctx):
    #     await Help.create_help(ctx, "claimchannel", "Channel Claiming", "Claims the current RP channel to a specific location.", parameters={"location": "The location of where you want the channel to be in. Surround the location with quotes (example: `\"Imagination Room\"`)."})
    
    # @help.command()
    # async def unclaimchannel(self, ctx):
    #     await Help.create_help(ctx, "unclaimchannel", "Channel Claiming", "Unclaims the RP channel.")
    
    # @help.command()
    # async def addclaimchannel(self, ctx):
    #     await Help.create_help(ctx, "addclaimchannel", "Channel Claiming", "Adds the RP channel to the bot.")
    
    # @help.command()
    # async def killswitch(self, ctx):
    #     await Help.create_help(ctx, "killswitch", "Moderation", "Shuts the bot down.", requireAdminRole=True)
    
    # @help.command()
    # async def restartswitch(self, ctx):
    #     await Help.create_help(ctx, "restartswitch", "Moderation", "Restarts the bot.", requireAdminRole=True)
    
    # @help.command()
    # async def hello(self, ctx):
    #     await Help.create_help(ctx, "hello", "Fun", "Sends a hello message! :D")

    # @help.command()
    # async def ping(self, ctx):
    #     await Help.create_help(ctx, "ping", "Fun", "I ping you back! :D")
    
    # @help.command()
    # async def bark(self, ctx):
    #     await Help.create_help(ctx, "bark", "Fun", "...why do you need help for a.. bark command..?")
        

def setup(bot):
    bot.add_cog(Help(bot))