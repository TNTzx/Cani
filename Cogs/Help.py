import discord
from discord.ext import commands

import main
from Functions import extraFunctions as ef

color = 0x7289da


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        main.bot.remove_command("help")

    listOfCommands = {
        "Channel Claiming": {
            "claimchannel": {
                "description": "Claims the current RP channel to a specific location.",
                "parameters": {
                    "location": "The location of where you want the channel to be in. Surround the location with quotes (example: `\"Imagination Room\"`)."
                }
            },
            "unclaimchannel": {
                "description": "Unclaims the RP channel."
            },
            "addclaimchannel":{
                "description": "Adds the RP channel to the bot.",
                "requireAdminRole": True
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
            }
        }
    }

    @main.bot.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(name="Help", title="Help!", description="what the dog doin", color=color)
        embed.set_footer(text=f"Type {main.commandPrefix}help <command> for more information to a command.")
        embed.add_field(name="Channel Claiming", value="`claimchannel`, `unclaimchannel`")
        embed.add_field(name="Moderation", value="`killswitch`, `restartswitch`")
        embed.add_field(name="Fun", value="`hello`, `ping`, `bark`")
        await ctx.send(embed=embed)

    
    async def create_help(ctx, commandName, category, description, parameters={}, requireAdminRole=False):
        embed = discord.Embed(name="Help", title=f"{category}: {main.commandPrefix}{commandName}", color=color)
        embed.add_field(name=f"Description", value=description)

        if requireAdminRole:
            embed.add_field(name=f"Required role:", value=f"`{main.adminRole}`", inline=False)

        if not len(parameters) == 0:
            parametersList = []
            parametersListKey = []
            for key, value in parameters.items():
                parametersList.append(f"`<{key}>`: {value}")
                parametersListKey.append(key)

            parametersListKeyFormatted = " ".join(parametersListKey)
            embed.add_field(name=f"Syntax:", value=f"`{main.commandPrefix}{commandName} <{parametersListKeyFormatted}>`", inline=False)

            parametersListFormatted = "\n".join(parametersList)
            embed.add_field(name=f"Parameters:", value=f"{parametersListFormatted}", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def claimchannel(self, ctx):
        await Help.create_help(ctx, "claimchannel", "Channel Claiming", "Claims the current RP channel to a specific location.", parameters={"location": "The location of where you want the channel to be in. Surround the location with quotes (example: `\"Imagination Room\"`)."})
    
    @help.command()
    async def unclaimchannel(self, ctx):
        await Help.create_help(ctx, "unclaimchannel", "Channel Claiming", "Unclaims the RP channel.")
    
    @help.command()
    async def addclaimchannel(self, ctx):
        await Help.create_help(ctx, "addclaimchannel", "Channel Claiming", "Adds the RP channel to the bot.")
    
    @help.command()
    async def killswitch(self, ctx):
        await Help.create_help(ctx, "killswitch", "Moderation", "Shuts the bot down.", requireAdminRole=True)
    
    @help.command()
    async def restartswitch(self, ctx):
        await Help.create_help(ctx, "restartswitch", "Moderation", "Restarts the bot.", requireAdminRole=True)
    
    @help.command()
    async def hello(self, ctx):
        await Help.create_help(ctx, "hello", "Fun", "Sends a hello message! :D")

    @help.command()
    async def ping(self, ctx):
        await Help.create_help(ctx, "ping", "Fun", "I ping you back! :D")
    
    @help.command()
    async def bark(self, ctx):
        await Help.create_help(ctx, "bark", "Fun", "...why do you need help for a.. bark command..?")
        

def setup(bot):
    bot.add_cog(Help(bot))