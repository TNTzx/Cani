# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-argument
# pylint: disable=no-self-use

import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import functions.firebase.firebase_interaction as f_i
import functions.other_functions as e_f
import functions.command_related.command_wrapper as c_w


class Barking(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot

    def bark_path(self, ctx: cmds.Context):
        return ["guilds", str(ctx.guild.id), "fun", "barking"]


    async def special_events(self, ctx: cmds.Context):
        path = self.bark_path(ctx)

        async def event_trigger(milestone, message):
            if f_i.get_data(path + ["totalBarks"]) >= milestone and (not f_i.get_data(path + ["barkMilestone"]) == milestone):
                await ctx.send("*>>> Oh? Something's happening...*")
                f_i.edit_data(path, {"barkMilestone": milestone})
                await ctx.send(message)

        await event_trigger(7500, ">>> YAYYAYAYAYYAAYAYA- AM HAPPY!! :D!!\n*Cani likes this server! The command `++pat` has been unlocked!*\n*Use `++help pat` for more information.*")


    async def update_bark(self, ctx: cmds.Context, add: int):
        path = self.bark_path(ctx)

        async def check_if_negative(bark_count):
            if bark_count < 0:
                bark_count = 0
            return bark_count


        if f_i.is_data_exists(path + ["users", str(ctx.author.id)]):
            bark_total = f_i.get_data(path + ["totalBarks"])
            bark_total += add
            bark_total = await check_if_negative(bark_total)
            f_i.edit_data(path, {"totalBarks": bark_total})

            bark_user = f_i.get_data(path + ["users", str(ctx.author.id), "barkCount"])
            bark_user += add
            bark_user = await check_if_negative(bark_user)
            f_i.edit_data(path + ["users", str(ctx.author.id)], {"barkCount": bark_user})
        else:
            bark_total = f_i.get_data(path + ["totalBarks"])
            bark_total += await check_if_negative(add)
            f_i.edit_data(path, {"totalBarks": bark_total})

            bark_user = await check_if_negative(add)
            default_data = {
                str(ctx.author.id): {
                    "barkCount": bark_user
                }
            }
            f_i.edit_data(path + ["users"], default_data)

        await self.special_events(ctx)


    @c_w.command(
        category=c_w.Categories.barking,
        description="Bark! :D",
        aliases=["b"],
        cooldown=2, cooldown_type=cmds.BucketType.user,
    )
    async def bark(self, ctx: cmds.Context):
        await ctx.send("*Bark! :D*")
        await self.update_bark(ctx, 1)


    @c_w.command(
        category=c_w.Categories.barking,
        description="Patpat! :D",
        cooldown=60 * 60 * 12, cooldown_type=cmds.BucketType.guild,
        show_condition=lambda ctx: f_i.get_data(Barking.bark_path(Barking(vrs.global_bot), ctx) + ["barkMilestone"]) >= 7500
    )
    async def pat(self, ctx: cmds.Context):
        add_bark = 50

        await ctx.send("https://cdn.discordapp.com/emojis/889713240714649650.gif")
        await ctx.send(f"""*:D!! Bark! Bark!*\n*I barked happily thanks to your pat! (+{add_bark} barks to {ctx.author.mention}!)*""")
        await self.update_bark(ctx, add_bark)


    @c_w.command(
        category=c_w.Categories.barking,
        description="Shows barking leaderboards!",
        aliases=["br"],
        cooldown=60 * 2, cooldown_type=cmds.BucketType.guild
    )
    async def barkrank(self, ctx: cmds.Context):
        await ctx.send("*Getting leaderboard...*")
        path = self.bark_path(ctx)

        users = f_i.get_data(path + ["users"])
        if users == "null":
            await e_f.sendError(ctx, "*There wasn't anyone that made me bark yet. Be the first one!*")
            return

        user_sort = sorted(users, key=lambda x: users[x]["barkCount"])
        user_sort.reverse()

        total_barks = f_i.get_data(path + ["totalBarks"])

        embed = nx.Embed(title="Leaderboard", title="Barking Leaderboard!", color=0x00FFFF)
        embed.add_field(name=f"Total Barks: {total_barks}", value="`----------`", inline=False)

        form_list = []
        for user_id in user_sort:
            user = await vrs.global_bot.fetch_user(user_id)
            user_barks = users[user_id]["barkCount"]
            form_list.append(f"{user_sort.index(user_id) + 1}. {user.name}: {user_barks}")

        form_str = "\n".join(form_list)
        embed.add_field(name="Leaderboard:", value=f"```{form_str}```", inline=False)
        embed.add_field(name="`----------`", value="_ _", inline=False)

        if str(ctx.author.id) in users:
            user_you = users[str(ctx.author.id)]["barkCount"]
            user_you_index = user_sort.index(str(ctx.author.id))
            user_you_pos = user_you_index + 1
        else:
            user_you = 0
            user_you_index = "?"
            user_you_pos = "?"

        async def bark_relative(pos, place):
            async def get_user(pos, offset):
                pos -= 1
                user = await vrs.global_bot.fetch_user(user_sort[pos + offset])
                user_barks = users[str(user.id)]["barkCount"]
                return user, user_barks

            if place == "up":
                user, user_barks = await get_user(pos, -1)
                return f"Next place up: `{pos - 1}. {user.name}: {user_barks}`"
            elif place == "down":
                user, user_barks = await get_user(pos, 1)
                return f"Previous place down: `{pos + 1}. {user.name}: {user_barks}`"


        if user_you_index == "?":
            desc_first = await bark_relative(len(user_sort), "up")
            desc_last = "You didn't make me bark yet!"
        elif user_you_index == 0:
            desc_first = await bark_relative(user_you_pos, "down")
            desc_last = "You're #1!"
        elif user_you_index == (len(user_sort) - 1):
            desc_first = await bark_relative(user_you_pos, "up")
            desc_last = "You're last place!"
        else:
            desc_first = await bark_relative(user_you_pos, "up")
            desc_last = await bark_relative(user_you_pos, "down")

        embed.add_field(name=f"Your total barks: {user_you} (#{user_you_pos})", value=f"{desc_first}\n{desc_last}", inline=False)

        await ctx.send(embed=embed)


    @c_w.command(
        category=c_w.Categories.barking,
        description="No. No. Please don't.",
        cooldown=60 * 2, cooldown_type=cmds.BucketType.guild
    )
    async def meow(self, ctx):
        await e_f.delay_message(ctx, "...")
        await e_f.delay_message(ctx, "...what did you just make me do.")
        await e_f.delay_message(ctx, "*grrrrrrrrrrRRRRRR**RRRRRRRRRR***", duration=1)
        await ctx.send("*(Art by glasses!)*")
        await e_f.delay_message(ctx, "https://cdn.discordapp.com/attachments/588692481001127936/867477895924154378/image0.png", duration=0.5)
        await e_f.delay_message(ctx, "**FEEL THE WRATH OF MY MACHINE GUN ATTACHMENTS, HUMAN**", duration=1)
        await e_f.delay_message(ctx, "*BULLET RAIN (-10 barks >:( )*", duration=2)
        await self.update_bark(ctx, -10)


def setup(bot):
    bot.add_cog(Barking(bot))
