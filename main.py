import discord
import discord.ext.commands as commands
import os
import asyncio

import KeepAlive

# UNCOMMENT SECOND TO LAST LINE WHEN UPDATING THE BOT!


commandPrefix = "++"
bot = discord.Client()
bot = commands.Bot(command_prefix=commandPrefix)
bot.remove_command("help")

adminRole = "///Moderator"

tntz = bot.fetch_user(279803094722674693)

def allCogs():
    return os.listdir(os.path.join(os.path.dirname(__file__), ".", "Cogs"))

for filename in allCogs():
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")

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

botToken = os.environ['CANITOKEN']
# KeepAlive.keep_alive()
bot.run(botToken)