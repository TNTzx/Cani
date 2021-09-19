import discord
from discord.ext import commands

import os
import sqlite3

from discord.message import Message

import main
from Functions import extraFunctions as eF
from Functions import sqlInteraction as sI

cooldownTime = 60 * 2

class ChannelClaim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    formatOfClaimDict = {
        "channel": {
            "claimStatus": False,
            "location": "Unknown"
        }
    }

    formatOfEmbedDict = {
        "channel": str,
        "messageId": int
    }


    async def getClaims(self, ctx):
        return sI.getData(ctx.guild.id, "claim_channel_data", type=dict)

    async def isRpChannel(self, ctx:commands.Context):
        channels = await self.getClaims(ctx)
        return ctx.channel.name in channels.keys()
        # return ctx.channel.name.startswith("general-rp-")


    async def editChannelDatabase(self, ctx, claimStatus, place):
        claimChannels = await self.getClaims(ctx)
        claimChannels[ctx.channel.name]["claimStatus"] = claimStatus
        claimChannels[ctx.channel.name]["location"] = place
        sI.editData(ctx.guild.id, claim_channel_data=claimChannels)
    

    async def updateEmbed(self, ctx):
        claimChannels = await self.getClaims(ctx)

        embed = discord.Embed(name="embed", title="Claimed Channels", color=0x0000ff)
        for key, value in claimChannels.items():
            if value["claimStatus"]:
                title = "Claimed"
                description = f"`Current location:` {value['location']}"
            else:
                title = "Unclaimed"
                description = f"_ _"
            
            newTitle = f"__#{key}__: {title}"
            embed.add_field(name=newTitle, value=description, inline=False)

        embedDict = sI.getData(ctx.guild.id, "claim_channel_embed", type=dict)
        embedChannel = await eF.getChannelFromMention(embedDict["channel"])
        mainEmbed = await embedChannel.fetch_message(embedDict["messageId"])

        await mainEmbed.edit(embed=embed)

    @commands.command(aliases=["cc"])
    @commands.guild_only()
    @commands.cooldown(1, cooldownTime, commands.BucketType.channel)
    async def claimchannel(self, ctx, type, place):
        if type == "claim":
            if await self.isRpChannel(ctx):
                await self.editChannelDatabase(ctx, True, place)
                await ctx.send(f"*Channel claimed! :D\nCurrent location: **{place}***")
            else:
                await eF.sendError(ctx, f"*This isn't an RP channel! >:(*")
        elif type == "unclaim":
            if await self.isRpChannel(ctx):
                claimChannels = await self.getClaims(ctx)
                if claimChannels[ctx.channel.name]["claimStatus"] == True:
                    await self.editChannelDatabase(ctx, False, "Unknown")
                    await ctx.send(f"*Channel unclaimed! :D*")
                else:
                    await eF.sendError(ctx, f"*This channel isn't claimed yet! >:(*")
            else:
                await eF.sendError(ctx, f"*This isn't an RP channel! >:(*")
        else:
            eF.sendError(ctx, f"*`{type}` isn't a valid argument! Type `{main.commandPrefix}help` for help!*")

        
        await self.updateEmbed(ctx)


    @commands.command(aliases=["ecc"])
    @commands.guild_only()
    @commands.has_role(main.adminRole)
    async def editclaimchannels(self, ctx:commands.Context, type, channelMention):
        claimChannels = await self.getClaims(ctx)
        try:
            channel = await eF.getChannelFromMention(channelMention)
        except ValueError:
            await eF.sendError(ctx, f"*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return

        if channel == None:
            await eF.sendError(ctx, f"*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return


        if type == "add":
            if not channel.name in claimChannels:
                await ctx.send("*Adding channel as an RP channel...*")
                claimChannels[channel.name] = {"claimStatus": False, "location": "Unknown"}
            else:
                await eF.sendError(ctx, f"*That channel is already added! >:(*")
                return
        elif type == "remove":
            if channel.name in claimChannels:
                await ctx.send("*Removing channel as an RP channel...*")
                claimChannels.pop(channel.name)
            else:
                await eF.sendError(ctx, f"*That channel hasn't been added yet! >:(*")
                return
        else:
            await eF.sendError(ctx, f"*`{type}` isn't a valid argument! Type `{main.commandPrefix}help` for help!*")
            return
        
        sI.editData(ctx.guild.id, claim_channel_data=claimChannels)

        if type == "add":
            await ctx.send("*The channel has been added as an RP channel! :D*")
        elif type == "remove":
            await ctx.send("*The channel has been removed as an RP channel! :D*")
        
        await self.updateEmbed(ctx)
    
    @commands.command()
    @commands.guild_only()
    @commands.has_role(main.adminRole)
    async def embedclaimchannel(self, ctx, channelMention):
        try:
            channel = await eF.getChannelFromMention(channelMention)
        except ValueError:
            await eF.sendError(ctx, f"*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return
        
        message = await channel.send(embed=discord.Embed(name="?", title="?", description="?"))

        sI.editData(ctx.guild.id, claim_channel_embed={
                "channel": channelMention,
                "messageId": message.id
            })

        await self.updateEmbed(ctx)
        await ctx.send(f"*Changed claim display channel to *{channelMention}*! :D*")
        
    

    @commands.command()
    @commands.guild_only()
    @commands.has_role(main.adminRole)
    async def causeerror(self, ctx):
        raise ValueError('funky error')
    
def setup(bot):
    bot.add_cog(ChannelClaim(bot))