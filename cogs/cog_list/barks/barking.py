"""Contains commands for barking."""


import nextcord.ext.commands as cmds

import backend.discord_utils as disc_utils
import backend.barking as barking
import backend.other_functions as o_f

from ... import utils as cog


class CogBark(cog.RegisteredCog):
    """Contains commands for barks."""
    def __init__(self, bot):
        self.bot = bot


    @disc_utils.command_wrap(
        category = disc_utils.CategoryBarking,
        cmd_info = disc_utils.CmdInfo(
            description = "bark",
            aliases = ["b"],
            cooldown_info = disc_utils.CooldownInfo(
                length = 2,
                type_ = cmds.BucketType.user
            )
        )
    )
    async def bark(self, ctx: cmds.Context):
        """bork"""
        await ctx.send("*Bark! :D*")
        await barking.STAT_TYPES.barks.add_stat(ctx, 1)


    @disc_utils.command_wrap(
        category = disc_utils.CategoryBarking,
        cmd_info = disc_utils.CmdInfo(
            description = "Patpat! :D",
            cooldown_info = disc_utils.CooldownInfo(
                length = 60 * 60 * 12,
                type_ = cmds.BucketType.guild
            ),
            usability_info = disc_utils.UsabilityInfo(
                usability_condition = lambda ctx: barking.STAT_TYPES.barks.server_scope.get_special_event("++pat").has_met_threshold(ctx)
            )
        )
    )
    async def pat(self, ctx: cmds.Context):
        """petpetpepteptpt"""
        add_bark = 50

        await ctx.send("https://cdn.discordapp.com/emojis/889713240714649650.gif")
        await ctx.send(f"""*:D!! Bark! Bark!*\n*I barked happily thanks to your pat! (+{add_bark} barks to {ctx.author.mention}!)*""")
        await barking.STAT_TYPES.barks.add_stat(ctx, add_bark)
        await barking.STAT_TYPES.pats.add_stat(ctx, 1)


    @disc_utils.command_wrap(
        category = disc_utils.CategoryBarking,
        cmd_info = disc_utils.CmdInfo(
            description = "stick collection! :D",
            cooldown_info = disc_utils.CooldownInfo(
                length = 60,
                type_ = cmds.BucketType.user
            ),
            usability_info = disc_utils.UsabilityInfo(
                usability_condition = lambda ctx: barking.STAT_TYPES.barks.server_scope.get_special_event("++fetch").has_met_threshold(ctx)
            )
        )
    )
    async def fetch(self, ctx: cmds.Context):
        """Fetch a stick!"""
        await ctx.send("*Hai, I have stick!*")
        await barking.STAT_TYPES.sticks.add_stat(ctx, 1)


    @disc_utils.command_wrap(
        category = disc_utils.CategoryBarking,
        cmd_info = disc_utils.CmdInfo(
            description = "No. No. Please don't.",
            cooldown_info = disc_utils.CooldownInfo(
                length = 60 * 2,
                type_ = cmds.BucketType.guild
            )
        )
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

        await barking.STAT_TYPES.meows.add_stat(ctx, 1)
        await barking.STAT_TYPES.barks.add_stat(ctx, -10)
