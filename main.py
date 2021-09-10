import discord
import discord.ext.commands
import os
import asyncio

commandPrefix = "//"
bot = discord.Client()
bot = discord.ext.commands.Bot(command_prefix=commandPrefix)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")


@bot.command()
async def hello(ctx):
    await ctx.send(f"*Bark! I'm an actual bot! :D*")

@bot.command()
async def claimchannel(ctx, place):
    currentTopic = ctx.channel.topic
    currentTopicSplit = currentTopic.split(" | ")
    newTopicList = [currentTopicSplit[0], " | ", f"Channel claimed. Current location: {place}"]

    await ctx.channel.edit(topic="".join(newTopicList))
    await ctx.send(f"Channel claimed.")


@bot.command()
async def killswitch(ctx):
    await ctx.send("O- *baiii-*")
    await bot.logout()

botToken = os.environ['CANITOKEN']
bot.run(botToken)