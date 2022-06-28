"""Module that contains decorators for choice parameters."""


import nextcord.ext.commands as nx_cmds

import backend.exc_utils as exc_utils
import backend.other as other


async def cmd_choice_check(ctx: nx_cmds.Context, parameter, choices: list):
    """Checks if `argument` is in `choices`. If the check fails, an error is sent to `ctx` then the command is exited."""
    try:
        other.choice_check(parameter, choices)
    except ValueError:
        await exc_utils.SendFailedCmd(
            error_place = exc_utils.ErrorPlace.from_context(ctx),
            suffix = (
                f"Make sure you have the correct parameters! `{parameter}` is not a valid parameter.\n"
                f"The available parameters are `{'`, `'.join(choices)}`."
            )
        ).send()
