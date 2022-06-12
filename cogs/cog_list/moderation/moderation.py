"""Moderation."""


import nextcord.ext.commands as cmds

import backend.discord_utils as disc_utils
import backend.firebase as firebase
import backend.exceptions.send_error as s_e

from ... import utils as cog


class CogModeration(cog.RegisteredCog):
    """Contains commands for moderation."""
    def __init__(self, bot):
        self.bot = bot

    @disc_utils.command_wrap(
        category = disc_utils.CategoryModeration,
        cmd_info = disc_utils.CmdInfo(
            description = "Sets the admin for the server.",
            params = disc_utils.Params(
                disc_utils.ParamArgument(
                    "id",
                    description = "The ID of the role you want to add. If you don't know how to get IDs, click `[here](https://support.discord.com/hc/en-us/community/posts/360048094171/comments/1500000318142)`."
                )
            ),
            perms = disc_utils.Permissions(
                [disc_utils.PermGuildOwner]
            )
        )
    )
    async def setadmin(self, ctx: cmds.Context, role_id):
        """Sets the admin for the server."""
        try:
            int(role_id)
        except ValueError:
            await s_e.send_error(ctx, "*You didn't send a valid role ID!*")
            return

        firebase.override_data(firebase.ShortEndpoint.discord_guilds.get_path() + [ctx.guild.id, 'admin_role'], role_id)
        await ctx.send("*The admin role for this server has been set! :D*")
