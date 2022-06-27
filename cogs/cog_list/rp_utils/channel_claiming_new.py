"""Contains the commands for channel claiming."""


import nextcord.ext.commands as nx_cmds

import global_vars
import backend.discord_utils as disc_utils

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
    async def claimchannel(self, ctx: nx_cmds.Context, action, place = None):
        """Claims a channel to a location."""

