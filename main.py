import discord
import discord.ext.commands as commands
import json
import pyrebase
import os
import asyncio
import KeepAlive

# UNCOMMENT SECOND TO LAST LINE WHEN UPDATING THE BOT!


def printIfHere(message):
    executedHere = __name__ == "__main__"
    if True:
        print(message)

commandPrefix = "++"
bot = discord.Client()
bot = commands.Bot(command_prefix=commandPrefix)
bot.remove_command("help")

adminRole = "///Moderator"

# Load all cogs
printIfHere("Loading cogs...")
def allCogs():
    return os.listdir(os.path.join(os.path.dirname(__file__), ".", "Cogs"))

for filename in allCogs():
    if filename.endswith(".py"):
        print(f"Loading cog '{filename}'...")
        bot.load_extension(f"Cogs.{filename[:-3]}")

printIfHere("Loaded all cogs!")


# Important commands
printIfHere("Loading important commands...")

@bot.command()
@commands.guild_only()
@commands.has_role(adminRole)
async def restartswitch(ctx):
    await ctx.send("*Restarting...*")

    for filename in allCogs():
        if filename.endswith(".py"):
            newName = f"Cogs.{filename[:-3]}"
            try:
                bot.unload_extension(newName)
            except commands.errors.ExtensionNotLoaded:
                continue
            bot.load_extension(newName)

    await ctx.send("*Restarted! :D*")
    print("\n \n Restart break! -------------------------------------- \n \n")

@bot.command()
@commands.guild_only()
@commands.has_role(adminRole)
async def killswitch(ctx):
    await ctx.send("O- *baiii-*")
    await bot.logout()

printIfHere("Loaded all important commands!")

# Server
printIfHere("Initializing server...")
# KeepAlive.keep_alive()
printIfHere("Initialized server!...")

# Log in
printIfHere("Logging into bot...")
botToken = os.environ['CANITOKEN']
bot.run(botToken)