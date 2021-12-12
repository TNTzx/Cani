# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-argument
# pylint: disable=no-self-use

import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import functions.command_related.command_wrapper as c_w
import functions.firebase.firebase_interaction as f_i
import functions.exceptions.custom_exc as c_e
import functions.exceptions.send_error as s_e
import functions.other_functions as o_f


class ChannelClaim(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def path(self, ctx: cmds.Context):
        return ["guilds", ctx.guild.id, "claimChannelData"]

    async def get_channels(self, ctx: cmds.Context):
        path = await self.path(ctx)
        data = f_i.get_data(path + ["availableChannels"])
        if not data == "null":
            return {
                channel["channelId"]: {
                    "claimStatus": channel["claimStatus"],
                    "location": channel["location"]
                    }
                for channel in data}
        else:
            return {}
    
    async def edit_claims(self, ctx: cmds.Context, data: dict[int, dict[str, bool | str]]):
        path = await self.path(ctx)
        new_data = [{
            "channelId": str(channel_id),
            "claimStatus": channel_data["claimStatus"],
            "location": channel_data["location"]
        } for channel_id, channel_data in data.items()]
        f_i.override_data(path + ["availableChannels"], new_data)

    async def is_rp_channel(self, ctx: cmds.Context):
        channels = await self.get_channels(ctx)
        return str(ctx.channel.id) in channels.keys()


    async def edit_channel_database(self, ctx: cmds.Context, claim_status, place, *dump):
        if len(place) >= 200:
            await s_e.send_error(ctx, "*You can't have locations with more than 200 characters! >:(*")
            raise c_e.ExitFunction("Exited Function.")

        channels = await self.get_channels(ctx)
        channels[str(ctx.channel.id)]["claimStatus"] = claim_status
        channels[str(ctx.channel.id)]["location"] = place
        await self.edit_claims(ctx, channels)


    async def update_embed(self, ctx: cmds.Context):
        path = await self.path(ctx)
        claim_channels = await self.get_channels(ctx)

        embed = nx.Embed(title="RP Channels", color=0x0000ff)

        if not len(claim_channels) == 0:
            for channel_id, data in claim_channels.items():
                if data["claimStatus"]:
                    title = "Claimed"
                    description = f"`Current location:` __{data['location']}__"
                else:
                    title = "Unclaimed"
                    description = "_ _"

                channel = vrs.global_bot.get_channel(int(channel_id))

                new_title = f"__#{channel.name}__: {title}"
                embed.add_field(name=new_title, value=description, inline=False)
        else:
            embed.add_field(name="No RP channels! :(", value=f"Ask the moderators to go add one using `{vrs.CMD_PREFIX}claimchanneledit add`.", inline=False)

        embed_info = f_i.get_data(path +  ["embedInfo"])
        if embed_info["channel"] == "null":
            await s_e.send_error(ctx, "*There hasn't been a channel added to display claimed channels. Please ask the moderators / admins to add one!*")
            return

        embed_channel = vrs.global_bot.get_channel(int(embed_info["channel"]))
        embed_message = await embed_channel.fetch_message(int(embed_info["messageId"]))

        await embed_message.edit(embed=embed)


    @c_w.command(
        category=c_w.Categories.channel_claiming,
        description="Claims / unclaims the current RP channel to a specific location.",
        parameters={
            "[claim | unclaim]": "Tells if you want to claim or unclaim the current RP channel.",
            "location": "The location of where you want the channel to be in. Surround the location with quotes (example: `\"Imagination Room\"`).\nNote that __this parameter doesn't have to be filled in when you're `unclaim`ing__ the channel."
        }, aliases=["cc"],
        cooldown=60 * 2, cooldown_type=cmds.BucketType.user,
        example_usage=[
            f"{vrs.CMD_PREFIX}claimchannel claim \"Quaz's HQ\"",
            f"{vrs.CMD_PREFIX}claimchannel unclaim"
        ])
    async def claimchannel(self, ctx: cmds.Context, action, place=None):
        if not await self.is_rp_channel(ctx):
            await s_e.send_error(ctx, "*This isn't an RP channel! >:(*", cooldown_reset=True)
            return

        async def claim():
            if not o_f.is_not_blank_str(place):
                await s_e.send_error(ctx, f"*You didn't specify what the `<location>` is! Type `{vrs.CMD_PREFIX}help` to get help! >:(*", cooldown_reset=True)
                return
            await ctx.send("*Claiming channel...*")
            await self.edit_channel_database(ctx, True, place)
            await ctx.send(f"*Channel claimed! :D\nCurrent location: __{place}__*")


        async def unclaim():
            claim_channels = await self.get_channels(ctx)
            if not claim_channels[str(ctx.channel.id)]["claimStatus"]:
                await s_e.send_error(ctx, "*This channel isn't claimed yet! >:(*", cooldown_reset=True)
                return

            await ctx.send("*Unclaiming channel...*")
            await self.edit_channel_database(ctx, False, "Unknown")
            await ctx.send("*Channel unclaimed! :D*")


        if action == "claim":
            await claim()
        elif action == "unclaim":
            await unclaim()
        else:
            await s_e.send_error(ctx, f"*`{action}` isn't a valid argument! Type `{vrs.CMD_PREFIX}help` for help!*", cooldown_reset=True)
            return

        await self.update_embed(ctx)


    @c_w.command(
        category=c_w.Categories.channel_claiming,
        description="Adds / removes the channel as an RP channel.",
        parameters={
            "[add | remove]": "Tells if you want to add or remove a channel as an RP channel.",
            "channel": "Channel that you want to add / remove as an RP channel."
        },
        aliases=["cce"],
        req_guild_admin=True
    )
    async def claimchanneledit(self, ctx: cmds.Context, action: str, channel_mention: str, *dump):
        path = await self.path(ctx)
        claim_channels = await self.get_channels(ctx)
        try:
            channel = await o_f.get_channel_from_mention(channel_mention)
        except ValueError:
            await s_e.send_error(ctx, "*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return

        if channel is None:
            await s_e.send_error(ctx, "*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return

        async def update_data(data):
            if not len(data) == 0:
                await self.edit_claims(ctx, data)
            else:
                f_i.edit_data(path, {"availableChannels": "null"})


        async def add():
            if str(channel.id) in claim_channels:
                await s_e.send_error(ctx, "*That channel is already added! >:(*")
                return

            await ctx.send("*Adding channel as an RP channel...*")
            claim_channels[channel.id] = {"claimStatus": False, "location": "Unknown"}
            await update_data(claim_channels)
            await ctx.send("*The channel has been added as an RP channel! :D*")


        async def remove():
            if not str(channel.id) in claim_channels:
                await s_e.send_error(ctx, "*That channel hasn't been added yet! >:(*")
                return

            await ctx.send("*Removing channel as an RP channel...*")
            claim_channels.pop(str(channel.id))
            await update_data(claim_channels)
            await ctx.send("*The channel has been removed as an RP channel! :D*")


        if action == "add":
            await add()
        elif action == "remove":
            await remove()
        else:
            await s_e.send_error(ctx, f"*`{action}` isn't a valid argument! Type `{vrs.CMD_PREFIX}help` for help!*")
            return

        await self.update_embed(ctx)

    @c_w.command(
        category=c_w.Categories.channel_claiming,
        description="Changes where the embed for displaying claimed channels are sent.",
        parameters={
            "channel": "Channel where the embed will be put in."
        },
        aliases=["ccm"],
        req_guild_admin=True
    )
    async def claimchannelembed(self, ctx: cmds.Context, channel_mention: str, *dump):
        path = await self.path(ctx)
        try:
            channel = await o_f.get_channel_from_mention(channel_mention)
        except ValueError:
            await s_e.send_error(ctx, "*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return

        message = await channel.send(embed=nx.Embed(title="?", description="?"))

        f_i.edit_data(path + ["embedInfo"], {
                "channel": str(channel.id),
                "messageId": str(message.id)
            })

        await ctx.send("*Changing claim display channel...*")
        await self.update_embed(ctx)
        await ctx.send(f"*Changed claim display channel to {channel_mention}! :D*")


    @c_w.command(
        category=c_w.Categories.channel_claiming,
        description="Updates the embed for displaying claimed channels.",
        aliases=["ccu"],
        req_guild_admin=True
    )
    async def claimchannelupdate(self, ctx: cmds.Context):
        await ctx.send("*Updating embed...*")
        await self.update_embed(ctx)
        await ctx.send("*Updated! :D*")

def setup(bot):
    bot.add_cog(ChannelClaim(bot))
