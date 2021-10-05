import discord
import discord.ext.commands as cmds

from Functions import ExtraFunctions as ef
from Functions import CommandWrappingFunction as cw


class Fun(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot


    @cw.command(
        category=cw.Categories.fun,
        description="I like pork!",
        cooldown=60 * 2, cooldownType=cmds.BucketType.guild
    )
    async def pork(self, ctx):
        await ef.delayMessage(ctx, f"https://media1.giphy.com/media/Lt3qObVV60Qda/200.gif", duration=7, delete=True)
        await ef.delayMessage(ctx, f"https://i.redd.it/bgmfikr8j9751.png", duration=2, delete=True)
        await ef.delayMessage(ctx, f"https://thumbs.gfycat.com/GreedyCourageousKrill-max-1mb.gif", duration=2)
        await ctx.send("*Yum!*")


def setup(bot):
    bot.add_cog(Fun(bot))