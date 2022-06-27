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
            # cooldown_info = disc_utils.CooldownInfo(
            #     length = 60 * 2,
            #     type_ = nx_cmds.BucketType.user
            # )
        )
    )
    async def claimchannel(self, ctx: nx_cmds.Context, action, place = claiming.DEFAULT_LOCATION):
        """Claims a channel to a location."""
        if action in ["claim", "unclaim"]:
            claim_status = action == "claim"
        else:
            await exc_utils.SendFailedCmd(
                error_place = exc_utils.ErrorPlace.from_context(ctx),
                suffix = f"`{action}` is not a valid action!"
            ).send()

        claim_data = claiming.ClaimData(
            claim_status = claim_status,
            location = place
        )

        claim_manager = claiming.ClaimChannelManager.from_guild_id(ctx.guild.id)
        claim_manager.claim_channels.get_claim_channel_by_id(ctx.channel.id).claim_data = claim_data
        await claim_manager.update_claim_channels(ctx.guild.id)
        await claim_manager.update_embed_safe(ctx)


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
