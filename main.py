import discord
import discord.ext.commands
import os

bot = discord.Client()
bot = discord.ext.commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")

@bot.command()
async def hello(ctx):
    await ctx.send(f"*Bark! I'm an actual bot! :D*")

@bot.command()
async def claimchannel(ctx, arg):
    ctx.channel.topic = arg
    

botToken = os.environ['TOKEN']
bot.run(botToken)