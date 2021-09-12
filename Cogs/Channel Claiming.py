import discord
from discord.ext import commands
import os
import asyncio
import main

async def isRpChannel(ctx):
    return ctx.channel.name.startswith("general-rp-")

class ChannelClaim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 60 * 5, commands.BucketType.channel)
    async def claimchannel(self, ctx, place):
        if await isRpChannel(ctx):
            currentTopic = ctx.channel.topic
            currentTopicSplit = currentTopic.split(" | ")
            newTopicList = [currentTopicSplit[0], " | ", f"Channel claimed. Current location: {place}"]

            await ctx.send(f"*Claiming...*")
            await ctx.channel.edit(topic="".join(newTopicList))
            await ctx.send(f"*Channel claimed! :D\nCurrent location: {place}*")
        else:
            await ctx.send(f"*This isn't an RP channel! >:(*")

    @commands.command()
    @commands.cooldown(1, 60 * 5, commands.BucketType.channel)
    async def unclaimchannel(self, ctx):
        if await isRpChannel(ctx):
            # get current topic
            currentTopic = ctx.channel.topic
            currentTopicSplit = currentTopic.split(" | ")

            if currentTopicSplit[1].startswith("Channel claimed. Current location:"):
                message = f"{currentTopicSplit[0]} | Channel unclaimed. Use {main.commandPrefix}claimchannel to claim this channel."
                await ctx.send(f"*Unclaiming...*")
                await ctx.channel.edit(topic=message)
                await ctx.send(f"*Channel unclaimed! :D*")
            else:
                await ctx.send(f"*This channel isn't claimed yet! >:(*")
        else:
            await ctx.send(f"*This isn't an RP channel! >:(*")
    
    @commands.command()
    @commands.has_role(main.adminRole)
    async def causeerror(self, ctx):
        raise ValueError('funky error')
    
    

def setup(bot):
    bot.add_cog(ChannelClaim(bot))