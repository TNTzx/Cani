import discord
import discord.ext.commands as cmds

import main
from GlobalVariables import defaultstuff as defaults
from Functions import CommandWrappingFunction as cw
from Functions import FirebaseInteraction as fi

async def updateData():
    for guild in main.bot.guilds:
        if not fi.isDataExists(["guilds", guild.id]):
            defaultValues = defaults.default["guildId"]
            defaultValues = {guild.id: defaultValues}
            fi.createData(["guilds"], defaultValues)

class Hello(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @cmds.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}.")
        await updateData()

    @cmds.Cog.listener()
    async def on_guild_join(self, guild):
        await updateData()


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
        requireGuildAdmin=True)
    async def updatedatabase(self, ctx):
        self.newDefault()
    
    @cw.command(
        category=cw.Categories.botControl,
        description="Causes an error! D:",
        requireGuildAdmin=True)
    async def causeerror(self, ctx):
        raise ValueError('funky error')

def setup(bot):
    bot.add_cog(Hello(bot))



