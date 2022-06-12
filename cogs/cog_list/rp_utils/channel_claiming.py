"""Contains commands for RP tools."""


import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars
import backend.discord_utils as disc_utils
import backend.rp_tools.channel_claiming as c_c
import backend.firebase as firebase
import backend.exceptions.send_error as s_e
import backend.other_functions as o_f

from ... import utils as cog


# REWRITE
class CogChannelClaiming(cog.RegisteredCog):
    """Contains commands for channel claiming."""
    def __init__(self, bot):
        self.bot = bot


    @disc_utils.command_wrap(
        category = disc_utils.CategoryChannelClaiming,
        cmd_info = disc_utils.CmdInfo(
            description = "Claims / unclaims the current RP channel to a specific location.",
            example = [
                f"{global_vars.CMD_PREFIX}claimchannel claim \"Quaz's HQ\"",
                f"{global_vars.CMD_PREFIX}claimchannel unclaim"
            ],
            params = disc_utils.Params(
                disc_utils.ParamsSplit(
                    disc_utils.Params(
                        disc_utils.ParamLiteral(
                            "claim",
                            description = "Claims this channel."
                        ),
                        disc_utils.ParamArgument(
                            "location",
                            description = "The location to claim this channel to."
                        )
                    ),
                    disc_utils.Params(
                        disc_utils.ParamLiteral(
                            "unclaim",
                            description = "Unclaims the current channel."
                        )
                    )
                )
            ),
            aliases = ["cc"],
            cooldown_info = disc_utils.CooldownInfo(
                length = 60 * 2,
                type_ = cmds.BucketType.user
            )
        )
    )
    async def claimchannel(self, ctx: cmds.Context, action, place=None):
        """Claims a channel to a location."""
        if not await c_c.is_rp_channel(ctx):
            await s_e.send_error(ctx, "*This isn't an RP channel! >:(*", cooldown_reset=True)
            return

        async def claim():
            if not o_f.is_not_blank_str(place):
                await s_e.send_error(ctx, f"*You didn't specify what the `<location>` is! Type `{global_vars.CMD_PREFIX}help` to get help! >:(*", cooldown_reset=True)
                return
            await ctx.send("*Claiming channel...*")
            await c_c.edit_channel_database(ctx, True, place)
            await ctx.send(f"*Channel claimed! :D\nCurrent location: __{place}__*")


        async def unclaim():
            claim_channels = await c_c.get_channels(ctx)
            if not claim_channels[str(ctx.channel.id)]["claim_status"]:
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
            await s_e.send_error(ctx, f"*`{action}` isn't a valid argument! Type `{global_vars.CMD_PREFIX}help` for help!*", cooldown_reset=True)
            return

        await c_c.update_embed(ctx)


    @disc_utils.command_wrap(
        category = disc_utils.CategoryChannelClaiming,
        cmd_info = disc_utils.CmdInfo(
            description = "Adds / removes the channel as an RP channel.",
            params = disc_utils.Params(
                disc_utils.ParamsSplit(
                    disc_utils.Params(
                        disc_utils.ParamLiteral(
                            "add",
                            description = "Adds a channel as an RP channel."
                        )
                    ),
                    disc_utils.Params(
                        disc_utils.ParamLiteral(
                            "remove",
                            description = "Removes a channel as an RP channel."
                        )
                    ),
                    description = "Tells if you want to add or remove a channel as an RP channel."
                ),
                disc_utils.ParamArgument(
                    "channel",
                    description = "Channel to add / remove."
                )
            ),
            aliases = ["cce"],
            perms = disc_utils.Permissions(
                [disc_utils.PermGuildAdmin]
            )
        )
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
                firebase.edit_data(path, {"availableChannels": firebase.PLACEHOLDER_DATA})


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
            await s_e.send_error(ctx, f"*`{action}` isn't a valid argument! Type `{global_vars.CMD_PREFIX}help` for help!*")
            return

        await c_c.update_embed(ctx)


    @disc_utils.command_wrap(
        category = disc_utils.CategoryChannelClaiming,
        cmd_info = disc_utils.CmdInfo(
            description = "Changes where the embed for displaying claimed channels are sent.",
            params = disc_utils.Params(
                disc_utils.ParamArgument(
                    "channel",
                    description = "Channel where the embed will be put in."
                )
            ),
            aliases = ["ccm"],
            perms = disc_utils.Permissions(
                [disc_utils.PermGuildAdmin]
            )
        )
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

        firebase.edit_data(path + ["embed_info"], {
                "channel_id": str(channel.id),
                "message_id": str(message.id)
            })

        await ctx.send("*Changing claim display channel...*")
        await c_c.update_embed(ctx)
        await ctx.send(f"*Changed claim display channel to {channel_mention}! :D*")


    @disc_utils.command_wrap(
        category = disc_utils.CategoryChannelClaiming,
        cmd_info = disc_utils.CmdInfo(
            description = "Updates the embed for displaying claimed channels.",
            aliases = ["ccu"],
            perms = disc_utils.Permissions(
                [disc_utils.PermGuildAdmin]
            )
        )
    )
    async def claimchannelupdate(self, ctx: cmds.Context):
        """Updates the embed."""
        await ctx.send("*Updating embed...*")
        await c_c.update_embed(ctx)
        await ctx.send("*Updated! :D*")
