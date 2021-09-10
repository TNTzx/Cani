import discord
from discord.ext import commands
import os
import asyncio
import main

commandPrefix = main.commandPrefix

async def isRpChannel(ctx):
    print(ctx.channel.name)
    return ctx.channel.name.startswith("general-rp-")

class ChannelClaim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def claimchannel(self, ctx, place):
        if await isRpChannel(ctx):
            currentTopic = ctx.channel.topic
            currentTopicSplit = currentTopic.split(" | ")
            newTopicList = [currentTopicSplit[0], " | ", f"Channel claimed. Current location: {place}"]

            await ctx.send(f"*Claiming...*")
            await ctx.channel.edit(topic="".join(newTopicList))
            await ctx.send(f"*Channel claimed. Current location: {place}*")
        else:
            await ctx.send(f"*This isn't an RP channel! >:(*")

    @commands.command()
    async def unclaimchannel(self, ctx):
        if await isRpChannel(ctx):
            currentTopic = ctx.channel.topic
            currentTopicSplit = currentTopic.split(" | ")

            if currentTopicSplit[1].startswith("Channel claimed. Current location:"):
                message = f"{currentTopicSplit[0]} | Channel unclaimed. Use {commandPrefix}claimchannel to claim this channel."
                await ctx.send(f"*Unclaiming...*")
                await ctx.channel.edit(topic=message)
                await ctx.send(f"*Channel unclaimed.*")
            else:
                await ctx.send(f"*The channel isn't claimed yet! >:(*")
        else:
            await ctx.send(f"*This isn't an RP channel! >:(*")
    
    

def setup(bot):
    bot.add_cog(ChannelClaim(bot))