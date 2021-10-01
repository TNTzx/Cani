import discord
import discord.ext.commands as cmds

import main
from Functions import firebaseInteraction as fi
from Functions import CustomExceptions as cE

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

    @cmds.command()
    async def hello(self, ctx):
        await ctx.send(f"*Bark! I'm an actual bot! :D*")

    @cmds.command()
    async def ping(self, ctx):
        await ctx.send(f"*Pong! <@{ctx.author.id}> :D*")
    
    @cmds.command(aliases=["ud"])
    @cmds.has_role(main.adminRole)
    async def updatedatabase(self, ctx):
        self.newDefault()
    
    @cmds.command()
    @cmds.guild_only()
    @cmds.has_role(main.adminRole)
    async def causeerror(self, ctx):
        raise ValueError('funky error')

def setup(bot):
    bot.add_cog(Hello(bot))



