import discord
import discord.ext.commands
import os
import asyncio

commandPrefix = "//"
bot = discord.Client()
bot = discord.ext.commands.Bot(command_prefix=commandPrefix)

adminRole = "beans"


def allCogs():
    return os.listdir(os.path.join(os.path.realpath(__file__), "..", "Cogs"))

for filename in allCogs():
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.command()
@discord.ext.commands.has_role(adminRole)
async def restartswitch(ctx):
    await ctx.send("*Restarting...*")

    for filename in allCogs():
        if filename.endswith(".py"):
            newName = f"Cogs.{filename[:-3]}"
            try:
                bot.unload_extension(newName)
            finally:
                bot.load_extension(newName)

    await ctx.send("*Restarted! :D*")

@bot.command()
@discord.ext.commands.has_role(adminRole)
async def killswitch(ctx):
    await ctx.send("O- *baiii-*")
    await bot.logout()

botToken = os.environ['CANITOKEN']
bot.run(botToken)