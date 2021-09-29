import discord
from discord.ext import commands

import main
from Functions import extraFunctions as eF
from Functions import firebaseInteraction as fi

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
        data = fi.getData(["guilds", ctx.guild.id, "claimChannelData", "availableChannels"])
        if not data == "null":
            return data
        else:
            return {}

    async def isRpChannel(self, ctx:commands.Context):
        channels = await self.getClaims(ctx)
        return ctx.channel.name in channels.keys()


    async def editChannelDatabase(self, ctx, claimStatus, place, *dump):
        claimChannels = await self.getClaims(ctx)
        claimChannels[ctx.channel.name]["claimStatus"] = claimStatus
        claimChannels[ctx.channel.name]["location"] = place
        fi.editData(["guilds", ctx.guild.id, "claimChannelData", "availableChannels"], claimChannels)
    

    async def updateEmbed(self, ctx):
        claimChannels = await self.getClaims(ctx)

        embed = discord.Embed(name="embed", title="Claimed Channels", color=0x0000ff)

        if not len(claimChannels) == 0:
            for key, value in claimChannels.items():
                if value["claimStatus"]:
                    title = "Claimed"
                    description = f"`Current location:` __{value['location']}__"
                else:
                    title = "Unclaimed"
                    description = f"_ _"
            
                newTitle = f"__#{key}__: {title}"
                embed.add_field(name=newTitle, value=description, inline=False)
        else:
            embed.add_field(name="No RP channels! :(", value=f"Ask the moderators to go add one using {main.commandPrefix}claimchanneledit add.", inline=False)

        embedDict = fi.getData(["guilds", ctx.guild.id, "claimChannelData", "embedInfo"])
        if embedDict["channel"] == "null":
            await eF.sendError(ctx, "*There hasn't been a channel added to display claimed channels. Please ask the moderators / admins to add one!*")
            return
        embedChannel = await eF.getChannelFromMention(embedDict["channel"])
        mainEmbed = await embedChannel.fetch_message(embedDict["messageId"])

        await mainEmbed.edit(embed=embed)


    @commands.command(aliases=["cc"])
    @commands.guild_only()
    @commands.cooldown(1, cooldownTime, commands.BucketType.user)
    async def claimchannel(self, ctx, type, place=None, *dump):
        if not await self.isRpChannel(ctx):
            await eF.sendError(ctx, f"*This isn't an RP channel! >:(*", resetCooldown=True)
            return

        if type == "claim":
            if not place == None:
                await ctx.send(f"*Claiming channel...*")
                await self.editChannelDatabase(ctx, True, place)
                await ctx.send(f"*Channel claimed! :D\nCurrent location: __{place}__*")
            else:
                await eF.sendError(ctx, f"*You didn't specify what the `<location>` is! Type `{main.commandPrefix}help` to get help! >:(*", resetCooldown=True, sendToAuthor=True)
                return
        elif type == "unclaim":
            claimChannels = await self.getClaims(ctx)
            if claimChannels[ctx.channel.name]["claimStatus"] == True:
                await ctx.send(f"*Unclaiming channel...*")
                await self.editChannelDatabase(ctx, False, "Unknown")
                await ctx.send(f"*Channel unclaimed! :D*")
            else:
                await eF.sendError(ctx, f"*This channel isn't claimed yet! >:(*", resetCooldown=True, sendToAuthor=True)
                return
        else:
            await eF.sendError(ctx, f"*`{type}` isn't a valid argument! Type `{main.commandPrefix}help` for help!*", resetCooldown=True, sendToAuthor=True)
            return

        await self.updateEmbed(ctx)


    @commands.command(aliases=["cce"])
    @commands.guild_only()
    @commands.has_role(main.adminRole)
    async def claimchanneledit(self, ctx, type, channelMention, *dump):
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
        
        if not len(claimChannels) == 0:
            fi.editData(["guilds", ctx.guild.id, "claimChannelData", "availableChannels"], claimChannels)
        else:
            fi.editData(["guilds", ctx.guild.id, "claimChannelData"], {"availableChannels": "null"})

        if type == "add":
            await ctx.send("*The channel has been added as an RP channel! :D*")
        elif type == "remove":
            await ctx.send("*The channel has been removed as an RP channel! :D*")
        
        await self.updateEmbed(ctx)


    @commands.command(aliases=["ccm"])
    @commands.guild_only()
    @commands.has_role(main.adminRole)
    async def claimchannelembed(self, ctx, channelMention, *dump):
        try:
            channel = await eF.getChannelFromMention(channelMention)
        except ValueError:
            await eF.sendError(ctx, f"*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return
        
        message = await channel.send(embed=discord.Embed(name="?", title="?", description="?"))

        fi.editData(["guilds", ctx.guild.id, "claimChannelData", "embedInfo"], {
                "channel": channelMention,
                "messageId": message.id
            })

        await ctx.send(f"*Changing claim display channel...*")
        await self.updateEmbed(ctx)
        await ctx.send(f"*Changed claim display channel to {channelMention}! :D*")
    

    @commands.command(aliases=["ccu"])
    @commands.guild_only()
    @commands.has_role(main.adminRole)
    async def claimchannelupdate(self, ctx):
        await ctx.send(f"*Updating embed...*")
        await self.updateEmbed(ctx)
        await ctx.send(f"*Updated! :D*")
        
    

    @commands.command()
    @commands.guild_only()
    @commands.has_role(main.adminRole)
    async def causeerror(self, ctx):
        raise ValueError('funky error')
    
def setup(bot):
    bot.add_cog(ChannelClaim(bot))