import discord
import discord.ext.commands
import os

bot = discord.Client()
bot = discord.ext.commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")

@bot.command()
async def helloWorld(ctx):
    await ctx.send(f"*Bark!* \n \"Your name must be {ctx.author}!")
    

botToken = os.environ['TOKEN']
bot.run(botToken)