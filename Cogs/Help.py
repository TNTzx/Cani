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
                    "[claim | unclaim]": "Tells if you want to claim or unclaim the current RP channel.",
                    "location": "The location of where you want the channel to be in. Surround the location with quotes (example: `\"Imagination Room\"`).\nNote that __this parameter doesn't have to be filled in when you're `unclaim`ing__ the channel."
                },
                "aliases": [
                    "cc"
                ],
                "cooldown": cc.cooldownTime,
                "exampleUsage": [
                    f"{main.commandPrefix}claimchannel claim \"Quaz's HQ\"",
                    f"{main.commandPrefix}claimchannel unclaim"
                ]
            },
            "claimchanneledit": {
                "description": "Adds / removes the channel as an RP channel.",
                "parameters": {
                    "[add | remove]": "Tells if you want to add or remove a channel as an RP channel.",
                    "channel": "Channel that you want to add / remove as an RP channel."
                },
                "requireAdminRole": True,
                "aliases": [
                    "cce"
                ],
                "exampleUsage": [
                    f"{main.commandPrefix}claimchanneledit add #general-rp-1",
                    f"{main.commandPrefix}claimchanneledit remove #general-rp-1"
                ]
            },
            "claimchannelembed": {
                "description": "Changes where the embed for displaying claimed channels are sent.",
                "parameters": {
                    "channel": "Channel where the embed will be put in."
                },
                "requireAdminRole": True,
                "aliases": [
                    "ccm"
                ],
                "exampleUsage": [
                    f"{main.commandPrefix}claimchannelembed #general-display"
                ]
            },
            "claimchannelupdate": {
                "description": "Updates the embed for displaying claimed channels.",
                "requireAdminRole": True,
                "aliases": [
                    "ccu"
                ]
            }
        },
        "Bot Control": {
            "switchkill": {
                "description": "Shuts the bot down.",
                "requireAdminRole": True,
                "aliases": [
                    "sk"
                ]
            },
            "switchrestart": {
                "description": "Restarts the bot.",
                "requireAdminRole": True,
                "aliases": [
                    "sr"
                ]
            },
            "updatedatabase": {
                "description": "Updates the database for new guilds.",
                "requireAdminRole": True,
                "aliases": [
                    "ud"
                ]
            }
        },
        "Basic Commands": {
            "hello": {
                "description": "Sends a hello message! :D"
            },
            "ping": {
                "description": "I ping you back! :D"
            },
            "help": {
                "description": "HOW THE HECK DID YOU GET HERE IF YOU'VE- WHAT- OH MY GOODNESS WHY- WHY DID YOU DO THIS-",
                "parameters": {
                    "[command]": "WHY DID YOU GET HELP FOR A HELP COMMAND ARE YOU I N S A N E"
                },
                "aliases": [
                    "h"
                ]
            }
        },
        "Fun": {
            "bark": {
                "description": "BARK",
                "parameters": {
                    "[rank]": "Displays barking leaderboards along with the total bark count! ~~WHY DID I DO THIS~~"
                },
                "aliases": [
                    "b"
                ],
                "cooldown": 2
            },
            "meow": {
                "description": "No. No. Please don't."
            },
            "pork": {
                "description": "Pork. That's it. That's all you get. Pork."
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
    

    @main.bot.group(invoke_without_command=True, aliases=["h"])
    async def help(self, ctx, *args):
        if not len(args) == 0:
            command = args[0]
            cmdDict, category = self.getCommand(command)
            if cmdDict == None:
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

            for category, commands in self.helpDict.items():
                commandFormat = f"`{'`, `'.join(commands.keys())}`"
                embed.add_field(name=category, value=commandFormat, inline=False)

            await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Help(bot))