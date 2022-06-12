"""Cog for bark rank."""


import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars
import backend.discord_utils as disc_utils
import backend.barking.path as p_b
import backend.barking.stat_types as s_t
import backend.barking.special_event as s_ev
import backend.exceptions.send_error as s_e
import backend.exceptions.custom_exc as c_e
import backend.firebase as firebase
import backend.other_functions as o_f

from ... import utils as cog


class CogBarkRank(cog.RegisteredCog):
    """Contains commands for bark rankings."""
    def __init__(self, bot):
        self.bot = bot


    @disc_utils.command_wrap(
        category = disc_utils.CategoryChannelClaiming
    )
    @c_w.command(
        category=c_w.Categories.barking,
        description="Shows barking leaderboards, as well as milestones!",
        parameters={
            "statistic name": "What statistic you need to view. Example, \"bark\" for the bark count. To view all `statistic name`s, simply type \"`++barkrank ?`\".",
            "[page]": "Page number of the leaderboard."
        },
        aliases=["br"],
        cooldown=30, cooldown_type=cmds.BucketType.guild
    )
    async def barkrank(self, ctx: cmds.Context, stat_type_name: str = "bark", page: int = 1):
        """Shows ranks for certain statistics."""
        page_length = 10

        stat_type_names = [stat_type.name for stat_type in s_t.STAT_TYPES.get_viewable_stat_types(ctx)]

        if stat_type_name == "?":
            await ctx.send(f"*The following statistics available are: `{'`, `'.join(stat_type_names)}`.*")
            return

        @c_p.choice_param_cmd(ctx, stat_type_name, stat_type_names)
        async def name():
            return s_t.STAT_TYPES.get_stat_type(stat_type_name)

        stat_type = await name()

        await ctx.send(f"*Getting leaderboard for `{stat_type.name}`...*")

        async def send_no_leaderboard_found():
            await s_e.send_error(ctx, f"*No leaderboard found for {stat_type.name}. Be the first one to be in that leaderboard!*")
            raise c_e.ExitFunction()

        users_data: dict[str, dict[str, dict[str, int]]] = firebase.get_data(p_b.get_path_users(ctx))
        if users_data is None:
            await send_no_leaderboard_found()


        server_total = stat_type.server_scope.get_total(ctx)


        def get_total_from_user_data(user_data_dict: dict):
            return user_data_dict[stat_type.name][stat_type.user_scope.raw.path_bundle.total[0]]


        embed = nx.Embed(
            title=f"{stat_type.name_plural_variations.case_sentence} Leaderboard!",
            color=0x00FFFF
        )

        def create_blank():
            embed.add_field(name="`----------`", value="_ _", inline=False)

        embed.add_field(name=f"Total {stat_type.name_plural_variations.case_sentence} in Server: {server_total}", value="`----------`", inline=False)


        def met_special_events_text(initial_name: str, met_special_events: list[s_ev.SpecialEvent]):
            if len(met_special_events) != 0:
                milestones_text = []
                for special_event in met_special_events:
                    milestones_text.append(f"{special_event.raw.name} ({special_event.raw.threshold} {stat_type.name_plural})")
                milestones_text = "\n".join(milestones_text)
                embed.add_field(name=f"{initial_name} milestones completed:", value=f"`{milestones_text}`", inline=False)
                return True
            return False

        has_met_special_events = [
            met_special_events_text("Server-wide", stat_type.server_scope.get_met_special_events(ctx)),
            met_special_events_text("User", stat_type.user_scope.get_met_special_events(ctx))
        ]

        if True not in has_met_special_events:
            embed.add_field(name="No milestones completed.. :(", value="_ _", inline=False)

        create_blank()

        users_data = {
            user_id: user_data
            for user_id, user_data in users_data.items()
            if stat_type.name in user_data
        }
        if len(users_data) == 0:
            await send_no_leaderboard_found()

        users_data = o_f.sort_dict_with_func(users_data, get_total_from_user_data, reverse=True)

        page_amount = o_f.page_amount(users_data, page_length)

        if page > page_amount:
            await s_e.send_error(ctx, "*There's no more pages past that! >:(*")
            return

        users_data_paged = o_f.get_page_dict(users_data, page - 1, page_length)


        def get_leaderboard():
            leaderboard = []
            for idx, user_data_tuple in enumerate(users_data_paged.items()):
                user_id = user_data_tuple[0]
                user = global_vars.global_bot.get_user(int(user_id))
                if user is not None:
                    user_name = user.name
                else:
                    user_name = "<unknown user>"
                user_total = get_total_from_user_data(user_data_tuple[1])
                leaderboard.append(f"{idx + 1 + ((page - 1) * page_length)}. {user_name}: {user_total}")

            leaderboard = '\n'.join(leaderboard)
            return leaderboard

        embed.add_field(name="Leaderboard:", value=f"```{get_leaderboard()}```", inline=False)

        create_blank()


        users_data_list = list(users_data.keys())
        try:
            author_index = users_data_list.index(str(ctx.author.id))
            author_place = author_index + 1
            author_total = get_total_from_user_data(users_data[str(ctx.author.id)])
        except ValueError:
            author_place = author_total = "?"

        # Keep in mind: an offset of -1 means you have a *higher* rank than someone, 1 means you have a *lower* rank
        # "Higher" means you're placed higher on the leaderboards.

        async def get_relative(pos: int, offset: int, display_bark_diff=True):
            relative_pos = pos + offset
            try:
                relative_id = users_data_list[relative_pos]
            except IndexError:
                return f"No one is {'above' if offset < 0 else 'below'} you!"
            relative = global_vars.global_bot.get_user(int(relative_id))
            if relative is not None:
                relative_name = relative.name
            else:
                relative_name = "<unknown user>"
            relative_barks = get_total_from_user_data(users_data[relative_id])

            if display_bark_diff:
                bark_diff_display = f" ({relative_barks - author_total} away)"
            else:
                bark_diff_display = ""

            relative_text = f"`{relative_pos + 1}. {relative_name}: {relative_barks}{bark_diff_display}`"
            if offset > 0:
                return f"Previous place down: {relative_text}"
            if offset < 0:
                return f"Next place up: {relative_text}"

        if str(ctx.author.id) in users_data:
            if author_index == 0:
                desc_first = await get_relative(author_index, 1)
                desc_last = "You're #1!"
            elif author_index == (len(users_data_list) - 1):
                desc_first = await get_relative(author_index, -1)
                desc_last = "You're last place!"
            else:
                desc_first = await get_relative(author_index, -1)
                desc_last = await get_relative(author_index, 1)
        else:
            desc_first = await get_relative(len(users_data_list), -1, display_bark_diff=False)
            desc_last = f"You don't have a statistic here yet! Try `{global_vars.CMD_PREFIX}help` to get help on how to enter!"


        embed.add_field(name=f"Your total {stat_type.name_plural}: {author_total} (#{author_place})", value=f"{desc_first}\n{desc_last}", inline=False)

        if page_amount > 1:
            embed.set_footer(text=f"Page {page} of {page_amount}. Use {global_vars.CMD_PREFIX}barkrank {stat_type.name} <page> to select a page.")

        await ctx.send(embed=embed)
