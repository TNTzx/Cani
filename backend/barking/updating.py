"""Backend for barking."""

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-statements
# pylint: disable=line-too-long


# import nextcord as nx
import nextcord.ext.commands as cmds

import backend.barking.special_events as s_ev
import backend.firebase.firebase_interaction as f_i


def bark_path(ctx: cmds.Context):
    """Gets the bark path."""
    return ["guilds", str(ctx.guild.id), "fun", "barking"]


async def trigger_special_events(ctx: cmds.Context):
    """Triggers a special event."""

    for event in s_ev.special_events:
        await event.event_trigger(ctx)


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
