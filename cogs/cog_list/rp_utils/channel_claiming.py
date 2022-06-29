"""Contains the commands for channel claiming."""


import nextcord.ext.commands as nx_cmds

import global_vars
import backend.discord_utils as disc_utils
import backend.exc_utils as exc_utils
import backend.rp_tools.channel_claiming as claiming

from ... import utils as cog


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
                    ),
                    description = "Determines if the action is to claim or unclaim the channel."
                )
            ),
            aliases = ["cc"],
            cooldown_info = disc_utils.CooldownInfo(
                length = 60 * 2,
                type_ = nx_cmds.BucketType.user
            )
        )
    )
    async def claimchannel(self, ctx: nx_cmds.Context, action, place = claiming.DEFAULT_LOCATION):
        """Claims a channel to a location."""
        place_len_limit = 500
        if len(place) > place_len_limit:
            await exc_utils.SendFailedCmd(
                error_place = exc_utils.ErrorPlace.from_context(ctx),
                suffix = f"The location can't be more than {place_len_limit} characters long!"
            ).send()

        await disc_utils.cmd_choice_check(ctx, action, ["claim", "unclaim"])
        claim_status = action == "claim"

        if claim_status and place == claiming.DEFAULT_LOCATION:
            await exc_utils.SendFailedCmd(
                error_place = exc_utils.ErrorPlace.from_context(ctx),
                suffix = "The location isn't specified! Specify the location if you're claiming the channel!"
            ).send()


        claim_manager = claiming.ClaimChannelManager.from_guild_id(ctx.guild.id)

        if not claim_manager.claim_channels.is_claimable_channel(ctx.channel.id):
            await exc_utils.SendFailedCmd(
                error_place = exc_utils.ErrorPlace.from_context(ctx),
                suffix = "This channel isn't a claimable channel! Add this channel as a claimable channel using `++claimchanneledit`!"
            ).send()

        claim_data = claiming.ClaimData(
            claim_status = claim_status,
            location = place
        )
        claim_channel = claim_manager.claim_channels.get_claim_channel_by_id(ctx.channel.id)

        if claim_channel.claim_data.claim_status == claim_data.claim_status == False:
            await exc_utils.SendFailedCmd(
                error_place = exc_utils.ErrorPlace.from_context(ctx),
                suffix = "This channel is already unclaimed!"
            ).send()

        claim_channel.claim_data = claim_data


        if claim_data.claim_status:
            await ctx.send(f"Claiming channel {ctx.channel.mention}...")
        else:
            await ctx.send(f"Unclaiming channel {ctx.channel.mention}...")

        await claim_manager.update_claim_channels(ctx.guild.id)
        await claim_manager.update_embed_safe(ctx)

        if claim_data.claim_status:
            await ctx.send(
                (
                    f"Channel {ctx.channel.mention} claimed!\n"
                    f"Location: `{place}`"
                )
            )
        else:
            await ctx.send(f"Channel {ctx.channel.mention} unclaimed!\n")


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
    async def claimchannelembed(self, ctx: nx_cmds.Context, channel_mention: str):
        """Changes the embed for the claim channels."""
        claim_manager = claiming.ClaimChannelManager.from_guild_id(ctx.guild.id)
        channel = await disc_utils.channel_from_id_warn(ctx, disc_utils.get_id_from_mention(channel_mention))
        await claim_manager.set_embed(ctx.guild.id, channel)


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
    async def claimchanneledit(self, ctx: nx_cmds.Context, action: str, channel_mention: str):
        """Edits possible claim channels."""
        await disc_utils.cmd_choice_check(ctx, action, ["add", "remove"])

        claim_manager = claiming.ClaimChannelManager.from_guild_id(ctx.guild.id)

        if action == "add":
            try:
                claim_manager.claim_channels.add_claim_channel(
                    disc_utils.get_id_from_mention(channel_mention)
                )
            except claiming.AlreadyClaimableChannel:
                await exc_utils.SendFailedCmd(
                    error_place = exc_utils.ErrorPlace.from_context(ctx),
                    suffix = f"The channel {channel_mention} is already a claimable channel!"
                ).send()
        else:
            try:
                claim_manager.claim_channels.remove_claim_channel(
                    disc_utils.get_id_from_mention(channel_mention)
                )
            except claiming.AlreadyNotClaimableChannel:
                await exc_utils.SendFailedCmd(
                    error_place = exc_utils.ErrorPlace.from_context(ctx),
                    suffix = f"The channel {channel_mention} is not a claimable channel!"
                ).send()

        prefix_pending = "Adding" if action == "add" else "Removing"
        await ctx.send(f"{prefix_pending} {channel_mention} as a claimable channel...")

        await claim_manager.update_claim_channels(ctx.guild.id)
        await claim_manager.update_embed_safe(ctx)

        prefix_success = "Added" if action == "add" else "Removed"
        await ctx.send(f"{prefix_success} {channel_mention} as a claimable channel!")


    @disc_utils.command_wrap(
        category = disc_utils.CategoryChannelClaiming,
        cmd_info = disc_utils.CmdInfo(
            description = "Orders the claimable channels in the embed into a specified order.",
            example = [
                f"{global_vars.CMD_PREFIX}claimchannelorder #rp-1 #rp-2 #rp-3 #rp-4"
            ],
            params = disc_utils.Params(
                disc_utils.ParamArgumentMultiple(
                    name = "channel mentions",
                    description = (
                        "The channel mentions of all claim channels in order from left to right.\n"
                        "This command will give an error if the channels you listed are "
                            "not in the list of claimable channels or "
                            "there are claimable channels not included in the list."
                    )
                )
            ),
            aliases = ["cco"],
            perms = disc_utils.Permissions(
                [disc_utils.PermGuildAdmin]
            )
        )
    )
    async def claimchannelorder(self, ctx: nx_cmds.Context, *channel_mentions: str):
        """Orders the channels in the embed into a specified order."""
        channel_ids = [disc_utils.get_id_from_mention(channel_mention) for channel_mention in channel_mentions]

        claim_manager = claiming.ClaimChannelManager.from_guild_id(ctx.guild.id)

        try:
            claim_manager.claim_channels.sort_claim_channels(channel_ids)
        except claiming.OrderListNotMatching:
            await exc_utils.SendFailedCmd(
                error_place = exc_utils.ErrorPlace.from_context(ctx),
                suffix = (
                    "The channels you listed don't match with the list of claimable channels!\n"
                    "Make sure your list:\n"
                    "- has all claimable channels in the server;"
                    "- has no duplicates; and"
                    "- has no channels that are not claimable!"
                )
            ).send()

        await claim_manager.update_claim_channels(ctx.guild.id)
        await claim_manager.update_embed_safe(ctx)

        await ctx.send("The claimable channels are now sorted!")
