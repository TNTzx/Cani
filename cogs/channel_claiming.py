"""Contains commands for RP tools."""


import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import global_vars.defaultstuff as df
import backend.command_related.command_wrapper as c_w
import backend.rp_tools.channel_claiming as c_c
import backend.firebase_new as firebase
import backend.exceptions.send_error as s_e
import backend.other_functions as o_f

# REWRITE
class ChannelClaiming(cmds.Cog):
    """Cog."""
    def __init__(self, bot):
        self.bot = bot


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
        """Claims a channel to a location."""
        if not await c_c.is_rp_channel(ctx):
            await s_e.send_error(ctx, "*This isn't an RP channel! >:(*", cooldown_reset=True)
            return

        async def claim():
            if not o_f.is_not_blank_str(place):
                await s_e.send_error(ctx, f"*You didn't specify what the `<location>` is! Type `{vrs.CMD_PREFIX}help` to get help! >:(*", cooldown_reset=True)
                return
            await ctx.send("*Claiming channel...*")
            await c_c.edit_channel_database(ctx, True, place)
            await ctx.send(f"*Channel claimed! :D\nCurrent location: __{place}__*")


        async def unclaim():
            claim_channels = await c_c.get_channels(ctx)
            if not claim_channels[str(ctx.channel.id)]["claimStatus"]:
                await s_e.send_error(ctx, "*This channel isn't claimed yet! >:(*", cooldown_reset=True)
                return

            await ctx.send("*Unclaiming channel...*")
            await c_c.edit_channel_database(ctx, False, "Unknown")
            await ctx.send("*Channel unclaimed! :D*")


        if action == "claim":
            await claim()
        elif action == "unclaim":
            await unclaim()
        else:
            await s_e.send_error(ctx, f"*`{action}` isn't a valid argument! Type `{vrs.CMD_PREFIX}help` for help!*", cooldown_reset=True)
            return

        await c_c.update_embed(ctx)


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
        """Edits possible claim channels."""
        path = await c_c.get_fb_path(ctx)
        claim_channels = await c_c.get_channels(ctx)
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
                await c_c.edit_claims(ctx, data)
            else:
                firebase.edit_data(path, {"availableChannels": df.PLACEHOLDER})


        async def add():
            if str(channel.id) in claim_channels:
                await s_e.send_error(ctx, "*That channel is already added! >:(*")
                return

            await ctx.send("*Adding channel as an RP channel...*")
            claim_channels[channel.id] = {"claim_status": False, "location": "Unknown"}
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

        await c_c.update_embed(ctx)

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
        """Changes the embed for the claim channels."""
        path = await c_c.get_fb_path(ctx)
        try:
            channel = await o_f.get_channel_from_mention(channel_mention)
        except ValueError:
            await s_e.send_error(ctx, "*The channel doesn't exist! Make sure the channel name is highlighted in blue!*")
            return

        message = await channel.send(embed=nx.Embed(title="?", description="?"))

        firebase.edit_data(path + ["embedInfo"], {
                "channel": str(channel.id),
                "messageId": str(message.id)
            })

        await ctx.send("*Changing claim display channel...*")
        await c_c.update_embed(ctx)
        await ctx.send(f"*Changed claim display channel to {channel_mention}! :D*")


    @c_w.command(
        category=c_w.Categories.channel_claiming,
        description="Updates the embed for displaying claimed channels.",
        aliases=["ccu"],
        req_guild_admin=True
    )
    async def claimchannelupdate(self, ctx: cmds.Context):
        """Updates the embed."""
        await ctx.send("*Updating embed...*")
        await c_c.update_embed(ctx)
        await ctx.send("*Updated! :D*")

def setup(bot: cmds.bot.Bot):
    """Setup.."""
    bot.add_cog(ChannelClaiming(bot))
