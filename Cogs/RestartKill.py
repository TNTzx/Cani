import discord
import discord.ext.commands as cmds
import os, sys

import main
from Functions import CommandWrappingFunction as cw


class RestartKill(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @cw.command(
        category=cw.Categories.botControl,
        description="Restarts the bot.",
        aliases=["sr"],
        requireDev=True
    )
    async def switchrestart(self, ctx):
        await ctx.send("*Restarting...*")
        main.restartSwitch()
        await ctx.send("*Restarted! :D*")
    

    @cw.command(
        category=cw.Categories.botControl,
        description="Shuts down the bot.",
        aliases=["sk"],
        requireDev=True
    )
    async def switchkill(self, ctx):
        await ctx.send("O- *baiii-*")
        await main.bot.logout()
    

    @cw.command(
        category=cw.Categories.botControl,
        description=f"Like {main.commandPrefix}restart, but hard.",
        aliases=["srh"],
        guildOnly=False,
        requireDev=True
    )
    async def switchrestarthard(self, ctx):
        await ctx.send("*Restart initiated! I'll be back in a bit! :D*")
        print("\n \n Restart break! Hard! -------------------------------------- \n \n")
        args = ['python'] + [f"\"{sys.argv[0]}\""]
        os.execv(sys.executable, args)
    
def setup(bot):
    bot.add_cog(RestartKill(bot))