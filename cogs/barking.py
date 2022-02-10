"""Contains commands for barking."""


import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import global_vars.defaultstuff as df
import backend.command_related.command_wrapper as c_w
import backend.barking.stat_types as s_t
import backend.barking.bark.updating as b_u
import backend.barking.special_events as s_ev
import backend.exceptions.send_error as s_e
import backend.firebase.firebase_interaction as f_i
import backend.other_functions as o_f


class Cog(cmds.Cog):
    """Cog."""
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
        show_condition=lambda ctx: f_i.get_data(b_u.bark_path(ctx) + ["barkMilestone"]) >= 2500
    )
    async def pat(self, ctx: cmds.Context):
        """petpetpepteptpt"""
        add_bark = 50

        await ctx.send("https://cdn.discordapp.com/emojis/889713240714649650.gif")
        await ctx.send(f"""*:D!! Bark! Bark!*\n*I barked happily thanks to your pat! (+{add_bark} barks to {ctx.author.mention}!)*""")
        await b_u.update_bark(ctx, add_bark)


    @c_w.command(
        category=c_w.Categories.barking,
        description="Shows barking leaderboards, as well as milestones!",
        parameters={
            "page": "Page number of the leaderboard."
        },
        aliases=["br"],
        cooldown=30, cooldown_type=cmds.BucketType.guild
    )
    async def barkrank(self, ctx: cmds.Context, page: int = 1):
        """Shows ranks for certain statistics."""
        page_length = 10

        await ctx.send("*Getting leaderboard...*")
        path = b_u.bark_path(ctx)

        bark_datas = f_i.get_data(path + ["users"])
        if bark_datas == df.PLACEHOLDER:
            await s_e.send_error(ctx, "*There wasn't anyone that made me bark yet. Be the first one!*")
            return


        total_barks = f_i.get_data(path + ["totalBarks"])

        embed = nx.Embed(title="Barking Leaderboard!", color=0x00FFFF)
        def create_blank():
            embed.add_field(name="`----------`", value="_ _", inline=False)

        embed.add_field(name=f"Total Barks in Server: {total_barks}", value="`----------`", inline=False)

        special_server_events_met = s_ev.get_met_special_events(total_barks)
        if len(special_server_events_met) != 0:
            milestones_text = []
            for special_event in special_server_events_met:
                milestones_text.append(f"{special_event.name} ({special_event.threshold} barks)")
            milestones_text = "\n".join(milestones_text)
            embed.add_field(name="Server-wide milestones completed:", value=f"`{milestones_text}`", inline=False)

        create_blank()


        bark_datas = o_f.sort_dict_with_func(bark_datas, lambda value: value["barkCount"], reverse=True)
        page_amount = o_f.page_amount(bark_datas, page_length)

        if page > page_amount:
            await s_e.send_error(ctx, "*There's no more pages past that! >:(*")
            return

        bark_datas_paged = o_f.get_page_dict(bark_datas, page - 1, page_length)

        leaderboard = []
        for idx, bark_data in enumerate(bark_datas_paged.items()):
            data_key = bark_data[0]
            user = vrs.global_bot.get_user(int(data_key))
            if user is not None:
                user_name = user.name
            else:
                user_name = "<unknown user>"
            data_value = bark_data[1]["barkCount"]
            leaderboard.append(f"{idx + 1 + ((page - 1) * page_length)}. {user_name}: {data_value}")

        leaderboard = '\n'.join(leaderboard)
        embed.add_field(name="Leaderboard:", value=f"```{leaderboard}```", inline=False)

        create_blank()


        bark_datas_list = list(bark_datas.keys())
        try:
            author_index = bark_datas_list.index(str(ctx.author.id))
            author_place = author_index + 1
            author_barks = bark_datas[str(ctx.author.id)]["barkCount"]
        except ValueError:
            author_place = author_barks = "?"

        # Keep in mind: an offset of -1 means you have a *higher* rank than someone, 1 means you have a *lower* rank
        # "Higher" means you're placed higher on the leaderboards.

        async def get_relative(pos: int, offset: int, display_bark_diff=True):
            relative_pos = pos + offset
            relative_id = bark_datas_list[relative_pos]
            relative = vrs.global_bot.get_user(int(relative_id))
            if relative is not None:
                relative_name = relative.name
            else:
                relative_name = "<unknown user>"
            relative_barks = bark_datas[relative_id]["barkCount"]

            if display_bark_diff:
                bark_diff_display = f" ({relative_barks - author_barks} away)"
            else:
                bark_diff_display = ""

            relative_text = f"`{relative_pos + 1}. {relative_name}: {relative_barks}{bark_diff_display}`"
            if offset > 0:
                return f"Previous place down: {relative_text}"
            if offset < 0:
                return f"Next place up: {relative_text}"

        if str(ctx.author.id) in bark_datas:
            if author_index == 0:
                desc_first = await get_relative(author_index, 1)
                desc_last = "You're #1!"
            elif author_index == (len(bark_datas_list) - 1):
                desc_first = await get_relative(author_index, -1)
                desc_last = "You're last place!"
            else:
                desc_first = await get_relative(author_index, -1)
                desc_last = await get_relative(author_index, 1)
        else:
            desc_first = await get_relative(len(bark_datas_list), -1, display_bark_diff=False)
            desc_last = "You didn't make me bark yet!"


        embed.add_field(name=f"Your total barks: {author_barks} (#{author_place})", value=f"{desc_first}\n{desc_last}", inline=False)

        if page_amount > 1:
            embed.set_footer(text=f"Page {page} of {page_amount}. Use {vrs.CMD_PREFIX}barkrank <page> to select a page.")

        await ctx.send(embed=embed)


    @c_w.command(
        category=c_w.Categories.barking,
        description="No. No. Please don't.",
        cooldown=60 * 2, cooldown_type=cmds.BucketType.guild
    )
    async def meow(self, ctx):
        """mrow"""
        await o_f.delay_message(ctx, "...")
        await o_f.delay_message(ctx, "...what did you just make me do.")
        await o_f.delay_message(ctx, "*grrrrrrrrrrRRRRRR**RRRRRRRRRR***", duration=1)
        await ctx.send("*(Art by glasses!)*")
        await o_f.delay_message(ctx, "https://cdn.discordapp.com/attachments/588692481001127936/867477895924154378/image0.png", duration=0.5)
        await o_f.delay_message(ctx, "**FEEL THE WRATH OF MY MACHINE GUN ATTACHMENTS, HUMAN**", duration=1)
        await o_f.delay_message(ctx, "*BULLET RAIN (-10 barks >:( )*", duration=2)
        await b_u.update_bark(ctx, -10)


def setup(bot):
    """Setup."""
    bot.add_cog(Cog(bot))
