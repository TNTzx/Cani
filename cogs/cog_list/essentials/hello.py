"""Contains events for on_ready and on_guild_join."""


import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars
import backend.discord_utils as disc_utils
import backend.firebase as firebase
import backend.barking as barking

from ... import utils as cog


async def add_new_to_database():
    """Updates the database for joined servers."""
    fb_path = firebase.ShortEndpoint.discord_guilds
    default_json = fb_path.get_default_data()
    default_json["fun"]["barking"]["server"] = {
        barking.STAT_TYPES.barks.name: barking.STAT_TYPES.barks.server_scope.raw.path_bundle.get_dict()
    }

    for guild in global_vars.global_bot.guilds:
        if not firebase.is_data_exists(fb_path.get_path() + [guild.id]):
            firebase.edit_data(fb_path.get_path() + [guild.id], {guild.id: default_json})


class CogEvents(cog.RegisteredCog):
    """A cog for events."""
    def __init__(self, bot):
        self.bot = bot


    @cmds.Cog.listener()
    async def on_ready(self):
        """On log-in."""
        print(f"Logged in as {global_vars.global_bot.user}.")
        global_vars.tntz = await global_vars.global_bot.fetch_user(279803094722674693)

        await global_vars.tntz.send("*Logged in! :D*")
        await add_new_to_database()

    @cmds.Cog.listener()
    async def on_guild_join(self, guild: nx.Guild):
        """On guild join."""
        await add_new_to_database()

    @disc_utils.command_wrap(
        category = disc_utils.CategoryBotControl,
        cmd_info = disc_utils.CmdInfo(
            description = "Updates the database juuuust in case my owner messed up.",
            usability_info = disc_utils.UsabilityInfo(
                guild_only = False
            ),
            perms = disc_utils.Permissions(
                [disc_utils.PermDev]
            )
        )
    )
    async def updatedatabase(self, ctx):
        """Updates the database."""
        await ctx.send("*Updating Database...*")
        await add_new_to_database()
        await ctx.send("*Updated! :D*")


    @disc_utils.command_wrap(
        category = disc_utils.CategoryBasics,
        cmd_info = disc_utils.CmdInfo(
            description = "Hello!",
        )
    )
    async def hello(self, ctx):
        """Hello there."""
        await ctx.send("*Bark! I'm an actual bot! :D*")

    @disc_utils.command_wrap(
        category = disc_utils.CategoryBasics,
        cmd_info = disc_utils.CmdInfo(
            description = "I ping you back! :D",
        )
    )
    async def ping(self, ctx):
        """ponge"""
        await ctx.send(f"*Pong! <@{ctx.author.id}> :D*")


    @disc_utils.command_wrap(
        category = disc_utils.CategoryBotControl,
        cmd_info = disc_utils.CmdInfo(
            description = "UAHEHG ERROR.",
            usability_info = disc_utils.UsabilityInfo(
                visible_in_help = False,
                guild_only = False
            ),
            perms = disc_utils.Permissions(
                [disc_utils.PermDev]
            )
        )
    )
    async def causeerror(self, ctx):
        """MOM HELP I'M AAAAAAAAAAAAAAAAAA"""
        raise ValueError('funky error')
