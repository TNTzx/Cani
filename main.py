import discord
import discord.ext.commands as commands
import os

from Functions import CommandWrapper as cw
import KeepAlive

commandPrefix = "++"
bot = discord.Client()
bot = commands.Bot(command_prefix=commandPrefix)
bot.remove_command("help")

adminRole = "///Moderator"

# Load all cogs
print("Loading cogs...")
def allCogs():
    return os.listdir(os.path.join(os.path.dirname(__file__), ".", "Cogs"))

for filename in allCogs():
    if filename.endswith(".py"):
        print(f"Loading cog '{filename}'...")
        bot.load_extension(f"Cogs.{filename[:-3]}")

print("Loaded all cogs!")


# Important commands
print("Loading important commands...")


@cw.command(
    category=cw.Categories.botControl,
    description="Restarts the bot.",
    aliases=["sr"],
    requireAdmin=True
)
async def switchrestart(ctx):
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

@cw.command(
    category=cw.Categories.botControl,
    description="Shuts down the bot.",
    aliases=["sk"],
    requireAdmin=True
)
async def switchkill(ctx):
    await ctx.send("O- *baiii-*")
    await bot.logout()

print("Loaded all important commands!")

# Server
print("Initializing server...")
# KeepAlive.keep_alive()
print("Initialized server!...")

# Log in
print("Logging into bot...")
botToken = os.environ['CANITOKEN']
bot.run(botToken)