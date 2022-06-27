"""Library for special events."""


import typing as typ
import nextcord.ext.commands as cmds

import backend.firebase as firebase

from . import path as path_m


class RawSpecialEvent():
    """Defines variables for the constructed special event."""
    def __init__(self, name, threshold: int, message: str, on_met: typ.Callable = lambda: None):
        self.name = name
        self.threshold = threshold
        self.message = message
        self.on_met = on_met


class SpecialEvent():
    """Parent class for special events."""
    def __init__(self, raw_special_event: RawSpecialEvent, path_bundle: path_m.PathBundle, category: str):
        self.raw = raw_special_event
        self.path_bundle = path_bundle
        self.category = category

    def get_initial_path(self, ctx: cmds.Context):
        """Gets the initial path for processing."""
        return path_m.get_fb_path(ctx)

    async def event_trigger(self, ctx: cmds.Context):
        """If the event meets the condition, the event is triggered."""
        fb_path = self.get_initial_path(ctx)
        if (firebase.get_data(fb_path + self.path_bundle.total, 0) >= self.raw.threshold) and \
                (not firebase.get_data(fb_path + self.path_bundle.milestone, 0) >= self.raw.threshold):
            await ctx.send("*> Oh? Something's happening...*")
            firebase.edit_data(fb_path, {self.path_bundle.milestone[0]: self.raw.threshold})
            await ctx.send(self.raw.message)

            self.raw.on_met()

    def has_met_threshold(self, ctx: cmds.Context):
        """Returns true if the threshold has been met."""
        return firebase.get_data(self.get_initial_path(ctx) + self.path_bundle.milestone, 0) >= self.raw.threshold


class ServerSpecialEvent(SpecialEvent):
    """Defines a special event for a server-wide count."""
    def get_initial_path(self, ctx: cmds.Context):
        return path_m.get_path_server(ctx, self.category)

class UserSpecialEvent(SpecialEvent):
    """Defines a special event for a user count on a statistic."""
    def get_initial_path(self, ctx: cmds.Context):
        return path_m.get_path_user(ctx, self.category)
