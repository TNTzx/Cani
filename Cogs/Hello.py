import discord
import discord.ext.commands as cmds

import main
from Functions import CommandWrapper as cw
from Functions import FirebaseInteraction as fi

class Hello(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot


    def newDefault(self):
        for guild in main.bot.guilds:
            if not fi.isDataExists(["guilds", guild.id]):
                defaultValues = {
                    guild.id: {
                        "claimChannelData": {
                            "availableChannels": "null",
                            "embedInfo": {
                                "channel": "null",
                                "messageId": "null"
                            }
                        },
                        "fun": {
                            "barking": {
                                "users": "null",
                                "totalBarks": 0
                            }, 
                        }
                    }
                }

                fi.editData(["guilds"], defaultValues)
    

    @cmds.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}.")

        for guild in main.bot.guilds:
            if not fi.isDataExists(["guilds", guild.id]):
                self.newDefault()


    @cw.command(
        category=cw.Categories.basicCommands,
        description="Hello!")
    async def hello(self, ctx):
        await ctx.send(f"*Bark! I'm an actual bot! :D*")

    @cw.command(
        category=cw.Categories.basicCommands,
        description="I ping you back! :D")
    async def ping(self, ctx):
        await ctx.send(f"*Pong! <@{ctx.author.id}> :D*")
    
    @cw.command(
        category=cw.Categories.botControl,
        description="Updates the database juuuust in case my owner messed up.",
        requireAdmin=True)
    async def updatedatabase(self, ctx):
        self.newDefault()
    
    @cw.command(
        category=cw.Categories.botControl,
        description="Causes an error! D:",
        requireAdmin=True)
    async def causeerror(self, ctx):
        raise ValueError('funky error')

def setup(bot):
    bot.add_cog(Hello(bot))



