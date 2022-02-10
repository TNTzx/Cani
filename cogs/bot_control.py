"""Contains commands for bot control."""


import os
import sys

import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import backend.command_related.command_wrapper as c_w


class BotControl(cmds.Cog):
    """Cog."""
    def __init__(self, bot: nx.Client):
        self.bot = bot

    @c_w.command(
        category=c_w.Categories.bot_control,
        description="Restarts the bot.",
        aliases=["sr"],
        guild_only=False,
        req_dev=True,
    )
    async def switchrestart(self, ctx):
        """Restarts the bot."""
        await ctx.send("Restarting bot...")
        for file in os.listdir(os.path.dirname(__file__)):
            if file.endswith(".py"):
                if file == "__init__.py":
                    continue
                new_file = f"{file[:-3]}"

                try:
                    self.bot.unload_extension(new_file)
                except cmds.errors.ExtensionNotLoaded:
                    continue
                self.bot.load_extension(new_file)
        await ctx.send("Restarted!")
        print("\n \n Restart break! -------------------------------------- \n \n")


    @c_w.command(
        category=c_w.Categories.bot_control,
        description="Shuts down the bot.",
        aliases=["sk"],
        guild_only=False,
        req_dev=True
    )
    async def switchkill(self, ctx):
        """Shuts the bot down."""
        await ctx.send("Terminated bot.")
        await self.bot.close()
        exit()


    @c_w.command(
        category=c_w.Categories.bot_control,
        description=f"Like {vrs.CMD_PREFIX}restart, but hard.",
        aliases=["srh"],
        guild_only=False,
        req_dev=True
    )
    async def switchrestarthard(self, ctx):
        """Restarts the bot harshly."""
        await ctx.send("Restart initiated!")
        print("\n \n Restart break! Hard! -------------------------------------- \n \n")
        args = ['python'] + [f"\"{sys.argv[0]}\""]
        os.execv(sys.executable, args)

def setup(bot):
    """Setup."""
    bot.add_cog(BotControl(bot))
