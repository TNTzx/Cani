"""Contains classes for scopes."""


import typing as typ
import nextcord as nx
import nextcord.ext.commands as cmds

import backend.barking.path as p_b
import backend.barking.special_event as s_ev
import backend.firebase.firebase_interaction as f_i


class RawScope():
    """Parent class of raw scopes. Used to construct the scope later on."""
    path_function: typ.Callable = None
    special_events_cls: typ.Type[s_ev.SpecialEvent] = None
    def __init__(self, path_bundle: p_b.PathBundle, raw_special_events: list[s_ev.RawSpecialEvent] = None):
        if raw_special_events is None:
            raw_special_events = []

        self.path_bundle = path_bundle
        self.raw_special_events = raw_special_events


class ServerRawScope(RawScope):
    """Class for server-wide raw scopes."""
    path_function = p_b.get_path_server
    special_events_cls = s_ev.ServerSpecialEvent

class UserRawScope(RawScope):
    """Class for user raw scopes."""
    path_function = p_b.get_path_user
    special_events_cls = s_ev.UserSpecialEvent


class Scope():
    """A class sbout a scope, server-wide, or users only."""
    def __init__(self, raw_scope: RawScope, category: str):
        self.raw = raw_scope
        self.category = category
        self.special_events = [
                raw_scope.special_events_cls(raw_special_event, raw_scope.path_bundle, category)
                for raw_special_event in raw_scope.raw_special_events
            ]

    async def add_on_scope(self, ctx: cmds.Context, amount: int):
        """Adds the amount to the scope."""
        path: list[str] = self.raw.path_function(ctx, self.category)
        if not f_i.is_data_exists(path):
            f_i.override_data(path, self.raw.path_bundle.get_dict())

        original_total = f_i.get_data(path + self.raw.path_bundle.total)
        new_total = original_total + amount
        f_i.override_data(path + self.raw.path_bundle.total, new_total)

        for special_event in self.special_events:
            await special_event.event_trigger(ctx)


    async def get_special_event(self, name: str):
        """Gets a special event by name from this scope."""
        for special_event in self.special_events:
            if special_event.raw.name == name:
                return special_event

        raise ValueError(f"Special event \"{name}\" not found in list of special events.")

    def get_met_special_events(self, ctx: cmds.Context):
        """Gets all met special events from this scope."""
        return [special_event.has_met_threshold(ctx) for special_event in self.special_events]

    def get_path(self, ctx: cmds.Context):
        """Gets the path to this scope."""
        return self.raw.path_function(ctx, self.category)
