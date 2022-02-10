"""Contains events for on_ready and on_guild_join."""


import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import global_vars.defaultstuff as defs
import backend.command_related.command_wrapper as c_w
import backend.firebase.firebase_interaction as f_i


async def update_data():
    """Updates the data."""
    for guild in vrs.global_bot.guilds:
        if not f_i.is_data_exists(["guilds", guild.id]):
            def_values = defs.default["guilds"]["guildId"]
            def_values = {guild.id: def_values}
            f_i.edit_data(["guilds"], def_values)


class Cog(cmds.Cog):
    """Cog."""
    def __init__(self, bot):
        self.bot = bot


    @cmds.Cog.listener()
    async def on_ready(self):
        """On log-in."""
        print(f"Logged in as {vrs.global_bot.user}.")
        vrs.tntz = await vrs.global_bot.fetch_user(279803094722674693)

        await vrs.tntz.send("*Logged in! :D*")
        await update_data()

    @cmds.Cog.listener()
    async def on_guild_join(self, guild: nx.Guild):
        """On guild join."""
        await update_data()

    @c_w.command(
        category=c_w.Categories.bot_control,
        description="Updates the database juuuust in case my owner messed up.",
        guild_only=False,
        req_dev=True
    )
    async def updatedatabase(self, ctx):
        """Updates the database."""
        await ctx.send("*Updating Database...*")
        await update_data()
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

def setup(bot: nx.Client):
    """Setup."""
    bot.add_cog(Cog(bot))
