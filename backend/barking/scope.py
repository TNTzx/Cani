"""Contains classes for scopes."""


import typing as typ

import nextcord.ext.commands as cmds

import backend.firebase as firebase

from . import path as path_m
from . import special_events


class RawScope():
    """Parent class of raw scopes. Used to construct the scope later on."""
    def __init__(self, path_bundle: path_m.PathBundle, raw_special_events: list[special_events.RawSpecialEvent] = None):
        if raw_special_events is None:
            raw_special_events = []

        self.path_function: typ.Callable = None
        self.special_events_cls: typ.Type[special_events.SpecialEvent] = None

        self.path_bundle = path_bundle
        self.raw_special_events = raw_special_events


class ServerRawScope(RawScope):
    """Class for server-wide raw scopes."""
    def __init__(self, path_bundle: path_m.PathBundle, raw_special_events: list[special_events.RawSpecialEvent] = None):
        super().__init__(path_bundle, raw_special_events)
        self.path_function = path_m.get_path_server
        self.special_events_cls = special_events.ServerSpecialEvent


class UserRawScope(RawScope):
    """Class for user raw scopes."""
    def __init__(self, path_bundle: path_m.PathBundle, raw_special_events: list[special_events.RawSpecialEvent] = None):
        super().__init__(path_bundle, raw_special_events)
        self.path_function = path_m.get_path_user
        self.special_events_cls = special_events.UserSpecialEvent


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
        fb_path: list[str] = self.raw.path_function(ctx, self.category)
        if not firebase.is_data_exists(fb_path):
            firebase.override_data(fb_path, self.raw.path_bundle.get_dict())

        original_total = firebase.get_data(fb_path + self.raw.path_bundle.total, 0)
        new_total = original_total + amount
        firebase.override_data(fb_path + self.raw.path_bundle.total, new_total)

        for special_event in self.special_events:
            await special_event.event_trigger(ctx)


    def get_path_value(self, ctx: cmds.Context, path_bundle_item: list[str]):
        """Gets the data from a path."""
        return firebase.get_data(self.get_path(ctx) + path_bundle_item)

    def get_total(self, ctx: cmds.Context):
        """Gets the total from this scope."""
        return self.get_path_value(ctx, self.raw.path_bundle.total)

    def get_milestone(self, ctx: cmds.Context):
        """Gets the milestone from this scope."""
        return self.get_path_value(ctx, self.raw.path_bundle.milestone)


    def get_special_event(self, name: str):
        """Gets a special event by name from this scope."""
        for special_event in self.special_events:
            if special_event.raw.name == name:
                return special_event

        raise ValueError(f"Special event \"{name}\" not found in list of special events.")

    def get_met_special_events(self, ctx: cmds.Context):
        """Gets all met special events from this scope."""
        return [special_event for special_event in self.special_events if special_event.has_met_threshold(ctx)]

    def get_path(self, ctx: cmds.Context):
        """Gets the path to this scope."""
        return self.raw.path_function(ctx, self.category)
