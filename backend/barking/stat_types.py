"""Contains statistic types."""


import typing as typ
import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.defaultstuff as df
import backend.barking.path as p_b
import backend.barking.new_special_event as s_e
import backend.firebase.firebase_interaction as f_i


class StatisticType():
    """A class for a statistic type such as "barks" and "pats"."""
    def __init__(
            self,
            name: str,
            path_server: p_b.PathBundle,
            path_user: p_b.PathBundle,
            server_raw_special_events: list[s_e.RawSpecialEvent] = None,
            user_raw_special_events: list[s_e.RawSpecialEvent] = None
            ):
        if server_raw_special_events is None:
            server_raw_special_events = []
        if user_raw_special_events is None:
            user_raw_special_events = []

        self.name = name

        self.server_path = path_server
        self.user_path = path_user

        def get_special_events(cls, raw_special_events: list[s_e.RawSpecialEvent]):
            return [
                cls(raw_special_event, path_server, name)
                for raw_special_event in raw_special_events
            ]

        self.server_special_events = get_special_events(s_e.ServerSpecialEvent, server_raw_special_events)
        self.user_special_events = get_special_events(s_e.UserSpecialEvent, user_raw_special_events)

    def add_stat(self, ctx: cmds.Context, amount: int):
        """Adds the amount to the stat."""

        def add_on_scope(path_function: typ.Callable, path_bundle: p_b.PathBundle, special_events: list[s_e.SpecialEvent]):
            path: list[str] = path_function(ctx, self.name)
            if not f_i.is_data_exists(path):
                f_i.override_data(path, path_bundle.get_dict())

            original_total = f_i.get_data(path + path_bundle.total)
            new_total = original_total + amount
            f_i.override_data(path + path_bundle.total, new_total)

            for special_event in special_events:
                special_event.event_trigger(ctx)

        add_on_scope(p_b.get_path_server, self.server_path, self.server_special_events)
        add_on_scope(p_b.get_path_user, self.user_path, self.user_special_events)


class StatisticTypes():
    """Contains the available statistic types."""
    def __init__(self):
        self.barks = StatisticType(
            "bark",
            p_b.DEFAULT_PATH_BUNDLE,
            p_b.DEFAULT_PATH_BUNDLE
        )

STAT_TYPES = StatisticTypes()