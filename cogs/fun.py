"""Fun commands!"""


import nextcord as nx
import nextcord.ext.commands as cmds

import backend.command_related.command_wrapper as c_w
import backend.other_functions as o_f


class Cog(cmds.Cog):
    """Cog."""
    def __init__(self, bot):
        self.bot = bot


    @c_w.command(
        category=c_w.Categories.fun,
        description="I like pork!",
        cooldown=60 * 2, cooldown_type=cmds.BucketType.guild
    )
    async def pork(self, ctx: cmds.Context):
        """PROK"""
        await o_f.delay_message(ctx, "https://media1.giphy.com/media/Lt3qObVV60Qda/200.gif", duration=7, delete=True)
        await o_f.delay_message(ctx, "https://i.redd.it/bgmfikr8j9751.png", duration=2, delete=True)
        await o_f.delay_message(ctx, "https://thumbs.gfycat.com/GreedyCourageousKrill-max-1mb.gif", duration=2)
        await ctx.send("*Yum!*")


def setup(bot: nx.Client):
    """Setup."""
    bot.add_cog(Cog(bot))
