# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-argument
# pylint: disable=no-self-use

# import nextcord as nx
import nextcord.ext.commands as cmds

import backend.command_related.command_wrapper as c_w
import backend.other_functions as o_f


class Fun(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot


    @c_w.command(
        category=c_w.Categories.fun,
        description="I like pork!",
        cooldown=60 * 2, cooldown_type=cmds.BucketType.guild
    )
    async def pork(self, ctx: cmds.Context):
        await o_f.delay_message(ctx, "https://media1.giphy.com/media/Lt3qObVV60Qda/200.gif", duration=7, delete=True)
        await o_f.delay_message(ctx, "https://i.redd.it/bgmfikr8j9751.png", duration=2, delete=True)
        await o_f.delay_message(ctx, "https://thumbs.gfycat.com/GreedyCourageousKrill-max-1mb.gif", duration=2)
        await ctx.send("*Yum!*")


def setup(bot):
    bot.add_cog(Fun(bot))
