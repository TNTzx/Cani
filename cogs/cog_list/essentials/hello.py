"""Contains events for on_ready and on_guild_join."""


import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import backend.command_related.command_wrapper as c_w
import backend.firebase as firebase
import backend.barking.stat_types as stats

from ... import utils as cog


# TEST
async def add_new_to_database():
    """Updates the database for joined servers."""
    fb_path = firebase.ShortEndpoint.discord_guilds
    default_json = fb_path.get_default_data()
    default_json["fun"]["barking"]["server"] = {
        stats.STAT_TYPES.barks.name: stats.STAT_TYPES.barks.server_scope.raw.path_bundle.get_dict()
    }

    for guild in vrs.global_bot.guilds:
        if not firebase.is_data_exists(fb_path.get_path() + [guild.id]):
            firebase.edit_data(fb_path.get_path() + [guild.id], {guild.id: default_json})


class CogEvents(cog.RegisteredCog):
    """A cog for events."""
    def __init__(self, bot):
        self.bot = bot


    @cmds.Cog.listener()
    async def on_ready(self):
        """On log-in."""
        print(f"Logged in as {vrs.global_bot.user}.")
        vrs.tntz = await vrs.global_bot.fetch_user(279803094722674693)

        await vrs.tntz.send("*Logged in! :D*")
        await add_new_to_database()

    @cmds.Cog.listener()
    async def on_guild_join(self, guild: nx.Guild):
        """On guild join."""
        await add_new_to_database()

    @c_w.command(
        category=c_w.Categories.bot_control,
        description="Updates the database juuuust in case my owner messed up.",
        guild_only=False,
        req_dev=True
    )
    async def updatedatabase(self, ctx):
        """Updates the database."""
        await ctx.send("*Updating Database...*")
        await add_new_to_database()
        await ctx.send("*Updated! :D*")


    @c_w.command(
        category=c_w.Categories.basic_commands,
        description="Hello!")
    async def hello(self, ctx):
        """Hello there."""
        await ctx.send("*Bark! I'm an actual bot! :D*")

    @c_w.command(
        category=c_w.Categories.basic_commands,
        description="I ping you back! :D")
    async def ping(self, ctx):
        """ponge"""
        await ctx.send(f"*Pong! <@{ctx.author.id}> :D*")


    @c_w.command(
        category=c_w.Categories.bot_control,
        description="Causes an error! D:",
        req_dev=True
    )
    async def causeerror(self, ctx):
        """MOM HELP I'M AAAAAAAAAAAAAAAAAA"""
        raise ValueError('funky error')
