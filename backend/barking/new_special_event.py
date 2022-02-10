"""Library for special events."""


import typing as typ
import nextcord as nx
import nextcord.ext.commands as cmds

import backend.firebase.firebase_interaction as f_i
import backend.barking.path as p_b


class RawSpecialEvent():
    """Defines variables for the constructed special event."""
    def __init__(self, name, threshold: int, message: str, on_met: typ.Callable = lambda: None):
        self.name = name
        self.threshold = threshold
        self.message = message
        self.on_met = on_met


class SpecialEvent():
    """Parent class for special events."""

    def __init__(self, raw_special_event: RawSpecialEvent, path_bundle: p_b.PathBundle, category: str):
        self.raw = raw_special_event
        self.path_bundle = path_bundle
        self.category = category

    def get_initial_path(self, ctx: cmds.Context):
        """Gets the initial path for processing."""
        return p_b.get_fb_path(ctx)

    async def event_trigger(self, ctx: cmds.Context):
        """If the event meets the condition, the event is triggered."""
        path = self.get_initial_path(ctx)
        if (f_i.get_data(path + self.path_bundle.total) >= self.raw.threshold) and \
                (not f_i.get_data(path + self.path_bundle.milestone) >= self.raw.threshold):
            await ctx.send("*> Oh? Something's happening...*")
            f_i.edit_data(path, {self.path_bundle.milestone: self.raw.threshold})
            await ctx.send(self.raw.message)

            self.raw.on_met()

    def has_met_threshold(self, ctx: cmds.Context):
        """Returns true if the threshold has been met."""
        return f_i.get_data(self.get_initial_path(ctx) + self.path_bundle.total) >= self.raw.threshold


class ServerSpecialEvent(SpecialEvent):
    """Defines a special event for a server-wide count."""
    def get_initial_path(self, ctx: cmds.Context):
        return p_b.get_path_server(ctx, self.category)

class UserSpecialEvent(SpecialEvent):
    """Defines a special event for a user count on a statistic."""
    def get_initial_path(self, ctx: cmds.Context):
        return p_b.get_path_user(ctx, self.category)
