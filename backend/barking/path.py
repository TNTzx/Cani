"""Defines path."""


import nextcord as nx
import nextcord.ext.commands as cmds


def get_fb_path(ctx: cmds.Context):
    """Get the firebase path."""
    return ["guilds", str(ctx.guild.id), "fun", "barking"]
