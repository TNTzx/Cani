"""Fun commands!"""


import nextcord.ext.commands as nx_cmds

import backend.discord_utils as disc_utils
import backend.other_functions as o_f

from ... import utils as cog


class CogFun(cog.RegisteredCog):
    """Fun cog!"""
    def __init__(self, bot):
        self.bot = bot


    @disc_utils.command_wrap(
        category = disc_utils.CategoryFun,
        cmd_info = disc_utils.CmdInfo(
            description = "I like pork!",
            cooldown_info = disc_utils.CooldownInfo(
                length = 60 * 2,
                type_ = nx_cmds.BucketType.guild
            )
        )
    )
    async def pork(self, ctx: nx_cmds.Context):
        """PROK"""
        await o_f.delay_message(ctx, "https://media1.giphy.com/media/Lt3qObVV60Qda/200.gif", duration=7, delete=True)
        await o_f.delay_message(ctx, "https://i.redd.it/bgmfikr8j9751.png", duration=2, delete=True)
        await o_f.delay_message(ctx, "https://thumbs.gfycat.com/GreedyCourageousKrill-max-1mb.gif", duration=2)
        await ctx.send("*Yum!*")
