import discord
from discord.ext import commands

import os
import sqlite3

import main
from Functions import extraFunctions as ef
from Functions import sqlInteraction as sI

cooldownTime = 60 * 2

class ChannelClaim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    {
        "general-rp-1": {
            "claimed": True,
            "location": "location!"
        }
    }

    async def isRpChannel(ctx:commands.Context):
        channels = sI.getData(ctx.guild.id)
        # return ctx.channel.name.startswith("general-rp-")

    

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, cooldownTime, commands.BucketType.channel)
    async def claimchannel(self, ctx, place):
        pass


        # if await self.isRpChannel(ctx):
        #     currentTopic = ctx.channel.topic
        #     currentTopicSplit = currentTopic.split(" | ")
        #     newTopicList = [currentTopicSplit[0], " | ", f"Channel claimed. Current location: {place}"]

        #     await ctx.send(f"*Claiming...*")
        #     await ctx.channel.edit(topic="".join(newTopicList))
        #     await ctx.send(f"*Channel claimed! :D\nCurrent location: {place}*")
        # else:
        #     await ef.sendError(ctx, f"*This isn't an RP channel! >:(*")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, cooldownTime, commands.BucketType.channel)
    async def unclaimchannel(self, ctx):
        if await self.isRpChannel(ctx):
            # get current topic
            currentTopic = ctx.channel.topic
            currentTopicSplit = currentTopic.split(" | ")

            if currentTopicSplit[1].startswith("Channel claimed. Current location:"):
                message = f"{currentTopicSplit[0]} | Channel unclaimed. Use {main.commandPrefix}claimchannel to claim this channel."
                await ctx.send(f"*Unclaiming...*")
                await ctx.channel.edit(topic=message)
                await ctx.send(f"*Channel unclaimed! :D*")
            else:
                await ef.sendError(ctx, f"*This channel isn't claimed yet! >:(*")
        else:
            await ef.sendError(ctx, f"*This isn't an RP channel! >:(*")
        

    @commands.command()
    @commands.guild_only()
    @commands.has_role(main.adminRole)
    async def addclaimchannel(self, ctx:commands.Context):
        channelName = ctx.channel.name
        self.channelClaimData[channelName] = {"claimStatus": False, "location": "Unknown"}
    
    @commands.command()
    @commands.guild_only()
    @commands.has_role(main.adminRole)
    async def causeerror(self, ctx):
        raise ValueError('funky error')
    
def setup(bot):
    bot.add_cog(ChannelClaim(bot))