"""Moderation."""


import nextcord.ext.commands as cmds

import backend.command_related.command_wrapper as c_w
import backend.firebase_new as firebase
import backend.exceptions.send_error as s_e

class Moderation(cmds.Cog):
    """Cog."""
    def __init__(self, bot):
        self.bot = bot

    @c_w.command(
        category=c_w.Categories.moderation,
        description="Sets the admin for the server.",
        parameters={"id": "The ID of the role you want to add. If you don't know how to get IDs, click [here](https://support.discord.com/hc/en-us/community/posts/360048094171/comments/1500000318142)."},
        req_guild_owner=True
    )
    async def setadmin(self, ctx: cmds.Context, role_id):
        """Sets the admin for the server."""
        try:
            int(role_id)
        except ValueError:
            await s_e.send_error(ctx, "*You didn't send a valid role ID!*")
            return

        firebase.edit_data(firebase.ShortEndpoint.discord_guilds.get_path() + [ctx.guild.id, 'admin_role'], role_id)
        await ctx.send("*The admin role for this server has been set! :D*")


def setup(bot: cmds.bot.Bot):
    """Setup."""
    bot.add_cog(Moderation(bot))
