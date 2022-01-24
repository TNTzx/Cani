"""Backend for barking."""

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-statements
# pylint: disable=line-too-long


from typing import Callable
# import nextcord as nx
import nextcord.ext.commands as cmds

import backend.firebase.firebase_interaction as f_i


def bark_path(ctx: cmds.Context):
    """Gets the bark path."""
    return ["guilds", str(ctx.guild.id), "fun", "barking"]


class SpecialEvent:
    """Class for special events."""
    def __init__(self, threshold: int, message: str, func: Callable = None):
        self.threshold = threshold
        self.message = message
        self.func = func

    async def event_trigger(self, ctx: cmds.Context):
        """Triggers the event if the threshold has been met once."""
        path = bark_path(ctx)
        if (f_i.get_data(path + ["totalBarks"]) >= self.threshold) and \
                (not f_i.get_data(path + ["barkMilestone"]) == self.threshold):
            await ctx.send("*>>> Oh? Something's happening...*")
            f_i.edit_data(path, {"barkMilestone": self.threshold})
            await ctx.send(self.message)

special_events = [
    SpecialEvent(2500, (
        ">>> YAYYAYAYAYYAAYAYA- AM HAPPY!! :D!!\n"
        "*Cani likes this server! The command `++pat` has been unlocked!*\n"
        "*Use `++help pat` for more information.*"
    ))
]


async def trigger_special_events(ctx: cmds.Context):
    """Triggers a special event."""

    for event in special_events:
        event.event_trigger(ctx)

    # async def event_trigger(milestone, message):
    #     if f_i.get_data(path + ["totalBarks"]) >= milestone and (not f_i.get_data(path + ["barkMilestone"]) == milestone):
    #         await ctx.send("*>>> Oh? Something's happening...*")
    #         f_i.edit_data(path, {"barkMilestone": milestone})
    #         await ctx.send(message)

    # await event_trigger(2500, (
    #     ">>> YAYYAYAYAYYAAYAYA- AM HAPPY!! :D!!\n"
    #     "*Cani likes this server! The command `++pat` has been unlocked!*\n"
    #     "*Use `++help pat` for more information.*"
    # ))


async def update_bark(ctx: cmds.Context, add: int):
    """Updates the bark count."""
    path = bark_path(ctx)

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

    await trigger_special_events(ctx)
