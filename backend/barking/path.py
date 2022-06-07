"""Defines path."""


import nextcord.ext.commands as cmds

import backend.firebase_new as firebase


def get_fb_path(ctx: cmds.Context):
    """Get the firebase path."""
    return firebase.ShortEndpoint.discord_guilds.get_path() + [str(ctx.guild.id), "fun", "barking"]

def get_path_server(ctx: cmds.Context, category: str):
    """Gets the path for the server-wide statistics."""
    return get_fb_path(ctx) + ["server", category]

def get_path_users(ctx: cmds.Context):
    """Gets the path for all users."""
    return get_fb_path(ctx) + ["users"]

def get_path_user(ctx: cmds.Context, category: str):
    """Gets the path for user statistics."""
    return get_path_users(ctx) + [str(ctx.author.id), category]


class PathBundle():
    """A class containing a path for total and milestone paths."""
    def __init__(self, path_total: str, path_milestone: str):
        self.total = [path_total]
        self.milestone = [path_milestone]

    def get_dict(self):
        """Gets the dictionary for path initialization."""
        return {
            self.total[0]: 0,
            self.milestone[0]: 0
        }

DEFAULT_PATH_BUNDLE = PathBundle("total", "milestone")
