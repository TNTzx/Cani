

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-statements
# pylint: disable=line-too-long


from typing import Callable
# import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import backend.firebase.firebase_interaction as f_i


class SpecialEvent:
    """Class for special events."""
    def __init__(self, name, threshold: int, message: str, func: Callable = None):
        self.name = name
        self.threshold = threshold
        self.message = message
        self.func = func

    async def event_trigger(self, ctx: cmds.Context):
        """Triggers the event if the threshold has been met once."""
        path = ["guilds", str(ctx.guild.id), "fun", "barking"]
        if (f_i.get_data(path + ["totalBarks"]) >= self.threshold) and \
                (not f_i.get_data(path + ["barkMilestone"]) >= self.threshold):
            await ctx.send("*>>> Oh? Something's happening...*")
            f_i.edit_data(path, {"barkMilestone": self.threshold})
            await ctx.send(self.message)

            self.func()

    def has_met_threshold(self, bark_count: int):
        """Returns true if the threshold has been met."""
        return bark_count >= self.threshold

special_events = [
    SpecialEvent(f"{vrs.CMD_PREFIX}pat", 2500, (
        ">>> YAYYAYAYAYYAAYAYA- AM HAPPY!! :D!!\n"
        "*Cani likes this server! The command `++pat` has been unlocked!*\n"
        f"*Use `{vrs.CMD_PREFIX}help pat` for more information.*"
    ))
]

def get_met_special_events(bark_count: int):
    """Gets all special events that have their thresholds met for a specific bark count."""
    return [special_event for special_event in special_events if special_event.has_met_threshold(bark_count)]