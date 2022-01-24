# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-argument
# pylint: disable=no-self-use

import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import global_vars.defaultstuff as defs
import backend.command_related.command_wrapper as c_w
import backend.firebase.firebase_interaction as f_i


async def update_data():
    for guild in vrs.global_bot.guilds:
        if not f_i.is_data_exists(["guilds", guild.id]):
            def_values = defs.default["guilds"]["guildId"]
            def_values = {guild.id: def_values}
            f_i.edit_data(["guilds"], def_values)

class Hello(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot


    @cmds.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {vrs.global_bot.user}.")
        await update_data()

    @cmds.Cog.listener()
    async def on_guild_join(self, guild: nx.Guild):
        await update_data()

    @c_w.command(
        category=c_w.Categories.bot_control,
        description="Updates the database juuuust in case my owner messed up.",
        guild_only=False,
        req_dev=True
    )
    async def updatedatabase(self, ctx):
        await ctx.send("*Updating Database...*")
        await update_data()
        await ctx.send("*Updated! :D*")


    @c_w.command(
        category=c_w.Categories.basic_commands,
        description="Hello!")
    async def hello(self, ctx):
        await ctx.send("*Bark! I'm an actual bot! :D*")

    @c_w.command(
        category=c_w.Categories.basic_commands,
        description="I ping you back! :D")
    async def ping(self, ctx):
        await ctx.send(f"*Pong! <@{ctx.author.id}> :D*")


    @c_w.command(
        category=c_w.Categories.bot_control,
        description="Causes an error! D:",
        req_dev=True
    )
    async def causeerror(self, ctx):
        raise ValueError('funky error')

def setup(bot):
    bot.add_cog(Hello(bot))
