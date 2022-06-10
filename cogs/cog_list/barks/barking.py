"""Contains commands for barking."""


import nextcord.ext.commands as cmds

import backend.command_related.command_wrapper as c_w
import backend.barking.stat_types as s_t
import backend.other_functions as o_f

from ... import utils as cog


class CogBark(cog.RegisteredCog):
    """Contains commands for barks."""
    def __init__(self, bot):
        self.bot = bot


    @c_w.command(
        category=c_w.Categories.barking,
        description="Bark! :D",
        aliases=["b"],
        cooldown=2, cooldown_type=cmds.BucketType.user,
    )
    async def bark(self, ctx: cmds.Context):
        """bork"""
        await ctx.send("*Bark! :D*")
        await s_t.STAT_TYPES.barks.add_stat(ctx, 1)


    @c_w.command(
        category=c_w.Categories.barking,
        description="Patpat! :D",
        cooldown=60 * 60 * 12, cooldown_type=cmds.BucketType.guild,
        show_condition=lambda ctx: s_t.STAT_TYPES.barks.server_scope.get_special_event("++pat").has_met_threshold(ctx)
    )
    async def pat(self, ctx: cmds.Context):
        """petpetpepteptpt"""
        add_bark = 50

        await ctx.send("https://cdn.discordapp.com/emojis/889713240714649650.gif")
        await ctx.send(f"""*:D!! Bark! Bark!*\n*I barked happily thanks to your pat! (+{add_bark} barks to {ctx.author.mention}!)*""")
        await s_t.STAT_TYPES.barks.add_stat(ctx, add_bark)
        await s_t.STAT_TYPES.pats.add_stat(ctx, 1)


    @c_w.command(
        category=c_w.Categories.barking,
        description="stick collection! :D",
        cooldown=60, cooldown_type=cmds.BucketType.user,
        show_condition=lambda ctx: s_t.STAT_TYPES.barks.server_scope.get_special_event("++fetch").has_met_threshold(ctx)
    )
    async def fetch(self, ctx: cmds.Context):
        """Fetch a stick!"""
        await ctx.send("*Hai, I have stick!*")
        await s_t.STAT_TYPES.sticks.add_stat(ctx, 1)


    @c_w.command(
        category=c_w.Categories.barking,
        description="No. No. Please don't.",
        cooldown=60 * 2, cooldown_type=cmds.BucketType.guild
    )
    async def meow(self, ctx: cmds.Context):
        """mrow"""
        await o_f.delay_message(ctx, "...")
        await o_f.delay_message(ctx, "...what did you just make me do.")
        await o_f.delay_message(ctx, "*grrrrrrrrrrRRRRRR**RRRRRRRRRR***", duration=1)
        await ctx.send("*(Art by glasses!)*")
        await o_f.delay_message(ctx, "https://cdn.discordapp.com/attachments/588692481001127936/867477895924154378/image0.png", duration=0.5)
        await o_f.delay_message(ctx, "**FEEL THE WRATH OF MY MACHINE GUN ATTACHMENTS, HUMAN**", duration=1)
        await o_f.delay_message(ctx, "*BULLET RAIN (-10 barks >:( )*", duration=2)

        await s_t.STAT_TYPES.meows.add_stat(ctx, 1)
        await s_t.STAT_TYPES.barks.add_stat(ctx, -10)
