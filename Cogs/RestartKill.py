import discord
import discord.ext.commands as cmds

import main
from Functions import CommandWrappingFunction as cw

class RestartKill(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @cw.command(
        category=cw.Categories.botControl,
        description="Restarts the bot.",
        aliases=["sr"],
        requireAdmin=True
    )
    async def switchrestart(self, ctx):
        await ctx.send("*Restarting...*")
        main.restartSwitch()
        await ctx.send("*Restarted! :D*")
    

    @cw.command(
        category=cw.Categories.botControl,
        description="Shuts down the bot.",
        aliases=["sk"],
        requireAdmin=True
    )
    async def switchkill(self, ctx):
        await ctx.send("O- *baiii-*")
        await main.bot.logout()
    
def setup(bot):
    bot.add_cog(RestartKill(bot))