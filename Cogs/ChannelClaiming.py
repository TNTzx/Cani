import discord
import discord.ext.commands as cmds

import main
from Functions import ExtraFunctions as ef
from Functions import FirebaseInteraction as fi
from Functions import CustomExceptions as ce
from Functions import CommandWrappingFunction as cw


class ChannelClaim(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def path(self, ctx: cmds.Context):
        return ["guilds", ctx.guild.id, "claimChannelData"]

    async def getChannels(self, ctx):
        path = await self.path(ctx)
        data = fi.getData(path + ["availableChannels"])
        if not data == "null":
            return data
        else:
            return {}

    async def isRpChannel(self, ctx: cmds.Context):
        channels = await self.getChannels(ctx)
        return str(ctx.channel.id) in channels.keys()


    async def editChannelDatabase(self, ctx, claimStatus, place, *dump):
        if len(place) >= 200:
            await ef.sendError(ctx, "*You can't have locations with more than 200 characters! >:(*")
            raise ce.ExitFunction("Exited Function.")

        path = await self.path(ctx)
        channels = await self.getChannels(ctx)
        channels[str(ctx.channel.id)]["claimStatus"] = claimStatus
        channels[str(ctx.channel.id)]["location"] = place
        fi.editData(path + ["availableChannels"], channels)
    

    async def updateEmbed(self, ctx):
        path = await self.path(ctx)
        claimChannels = await self.getChannels(ctx)

        embed = discord.Embed(name="embed", title="RP Channels", color=0x0000ff)

        if not len(claimChannels) == 0:
            for channelId, data in claimChannels.items():
                if data["claimStatus"]:
                    title = "Claimed"
                    description = f"`Current location:` __{data['location']}__"
                else:
                    title = "Unclaimed"
                    description = f"_ _"

                channel = main.bot.get_channel(int(channelId))

                newTitle = f"__#{channel.name}__: {title}"
                embed.add_field(name=newTitle, value=description, inline=False)
        else:
            embed.add_field(name="No RP channels! :(", value=f"Ask the moderators to go add one using {main.commandPrefix}claimchanneledit add.", inline=False)

        embedInfo = fi.getData(path +  ["embedInfo"])
        if embedInfo["channel"] == "null":
            await ef.sendError(ctx, "*There hasn't been a channel added to display claimed channels. Please ask the moderators / admins to add one!*")
            return

        embedChannel = main.bot.get_channel(embedInfo["channel"])
        embedMessage = await embedChannel.fetch_message(embedInfo["messageId"])

        await embedMessage.edit(embed=embed)


    @cw.command(
        category=cw.Categories.channelClaiming,
        description="Claims / unclaims the current RP channel to a specific location.",
        parameters={
            "[claim | unclaim]": "Tells if you want to claim or unclaim the current RP channel.",
            "location": "The location of where you want the channel to be in. Surround the location with quotes (example: `\"Imagination Room\"`).\nNote that __this parameter doesn't have to be filled in when you're `unclaim`ing__ the channel."
        }, aliases=["cc"],
        cooldown=60 * 2, cooldownType=cmds.BucketType.user,
        exampleUsage=[
            f"{main.commandPrefix}claimchannel claim \"Quaz's HQ\"",
            f"{main.commandPrefix}claimchannel unclaim"
        ])
    async def claimchannel(self, ctx, type, place=None, *dump):
        if not await self.isRpChannel(ctx):
            await ef.sendError(ctx, f"*This isn't an RP channel! >:(*", resetCooldown=True)
            return

        async def claim():
            if place == None:
                await ef.sendError(ctx, f"*You didn't specify what the `<location>` is! Type `{main.commandPrefix}help` to get help! >:(*", resetCooldown=True, sendToAuthor=True)
                return
            await ctx.send(f"*Claiming channel...*")
            await self.editChannelDatabase(ctx, True, place)
            await ctx.send(f"*Channel claimed! :D\nCurrent location: __{place}__*")
                
        
        async def unclaim():
            claimChannels = await self.getChannels(ctx)
            if not claimChannels[str(ctx.channel.id)]["claimStatus"] == True:
                await ef.sendError(ctx, f"*This channel isn't claimed yet! >:(*", resetCooldown=True, sendToAuthor=True)
                return
    
            await ctx.send(f"*Unclaiming channel...*")
            await self.editChannelDatabase(ctx, False, "Unknown")
            await ctx.send(f"*Channel unclaimed! :D*")
                

        if type == "claim":
            await claim()
        elif type == "unclaim":
            await unclaim()
        else:
            await ef.sendError(ctx, f"*`{type}` isn't a valid argument! Type `{main.commandPrefix}help` for help!*", resetCooldown=True, sendToAuthor=True)
            return

        await self.updateEmbed(ctx)


    @cw.command(
        category=cw.Categories.channelClaiming,
        description="Adds / removes the channel as an RP channel.",
        parameters={
            "[add | remove]": "Tells if you want to add or remove a channel as an RP channel.",
            "channel": "Channel that you want to add / remove as an RP channel."
        },
        aliases=["cce"],
        requireGuildAdmin=True
    )
    async def claimchanneledit(self, ctx, type, channelMention, *dump):
        path = await self.path(ctx)
        claimChannels = await self.getChannels(ctx)
        try:
            channel = await ef.getChannelFromMention(channelMention)
        except ValueError:
            await ef.sendError(ctx, f"*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return

        if channel == None:
            await ef.sendError(ctx, f"*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return
        
        async def updateData(data):
            if not len(data) == 0:
                fi.editData(path + ["availableChannels"], data)
            else:
                fi.editData(path, {"availableChannels": "null"})


        async def add():
            if channel.id in claimChannels:
                await ef.sendError(ctx, f"*That channel is already added! >:(*")
                return

            await ctx.send("*Adding channel as an RP channel...*")
            claimChannels[channel.id] = {"claimStatus": False, "location": "Unknown"}
            await updateData(claimChannels)
            await ctx.send("*The channel has been added as an RP channel! :D*")

        async def remove():
            if not channel.id in claimChannels:
                await ef.sendError(ctx, f"*That channel hasn't been added yet! >:(*")
                return

            await ctx.send("*Removing channel as an RP channel...*")
            claimChannels.pop(channel.id)
            await updateData(claimChannels)
            await ctx.send("*The channel has been removed as an RP channel! :D*")
  

        if type == "add":
            await add()
        elif type == "remove":
            await remove()
        else:
            await ef.sendError(ctx, f"*`{type}` isn't a valid argument! Type `{main.commandPrefix}help` for help!*")
            return
        
        await self.updateEmbed(ctx)

    @cw.command(
        category=cw.Categories.channelClaiming,
        description="Changes where the embed for displaying claimed channels are sent.",
        parameters={
            "channel": "Channel where the embed will be put in."
        },
        aliases=["ccm"],
        requireGuildAdmin=True
    )
    async def claimchannelembed(self, ctx, channelMention, *dump):
        path = await self.path(ctx)
        try:
            channel = await ef.getChannelFromMention(channelMention)
        except ValueError:
            await ef.sendError(ctx, f"*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return
        
        message = await channel.send(embed=discord.Embed(name="?", title="?", description="?"))

        fi.editData(path + ["embedInfo"], {
                "channel": channel.id,
                "messageId": message.id
            })

        await ctx.send(f"*Changing claim display channel...*")
        await self.updateEmbed(ctx)
        await ctx.send(f"*Changed claim display channel to {channelMention}! :D*")
    

    @cw.command(
        category=cw.Categories.channelClaiming,
        description="Updates the embed for displaying claimed channels.",
        aliases=["ccu"],
        requireGuildAdmin=True
    )
    async def claimchannelupdate(self, ctx):
        await ctx.send(f"*Updating embed...*")
        await self.updateEmbed(ctx)
        await ctx.send(f"*Updated! :D*")
    
def setup(bot):
    bot.add_cog(ChannelClaim(bot))