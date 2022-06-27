"""Contains statistic types."""


import nextcord.ext.commands as cmds

import global_vars

import backend.main_classes.str_variations as str_v
import backend.firebase as firebase

from . import path as path_m
from . import special_events
from . import scope


class StatisticType():
    """A class for a statistic type such as "barks" and "pats"."""
    def __init__(self, name: str, name_plural: str, server_raw_scope: scope.ServerRawScope, user_raw_scope: scope.UserRawScope):
        self.name = name
        self.name_variations = str_v.StrVariations(name)
        self.name_plural = name_plural
        self.name_plural_variations = str_v.StrVariations(name_plural)

        def get_scope(raw_scope: scope.RawScope):
            return scope.Scope(raw_scope, name)

        self.server_scope = get_scope(server_raw_scope)
        self.user_scope = get_scope(user_raw_scope)


    async def add_stat(self, ctx: cmds.Context, amount: int):
        """Adds the amount to the stat."""
        for scope in [self.server_scope, self.user_scope]:
            await scope.add_on_scope(ctx, amount)

    def is_unlocked(self, ctx: cmds.Context):
        """Checks if the stat is unlocked."""
        return firebase.is_data_exists(self.server_scope.get_path(ctx))


class StatisticTypes():
    """Contains the available statistic types."""
    def __init__(self):
        self.barks = StatisticType(
            "bark", "barks",
            server_raw_scope = scope.ServerRawScope(
                path_m.DEFAULT_PATH_BUNDLE,
                raw_special_events = [
                    special_events.RawSpecialEvent(
                        "++pat", 1000, (
                            ">>> YAYYAYAYAYYAAYAYA- AM HAPPY!! :D!!\n"
                            "*Cani likes this server! The command `++pat` has been unlocked!*\n"
                            f"*Use `{global_vars.CMD_PREFIX}help pat` for more information.*"
                        )
                    ),
                    special_events.RawSpecialEvent(
                        "++fetch", 2500, (
                            ">>> ...oooh, a.. stick!\n"
                            "*Cani found some sticks for this server! The command `++fetch` has been unlocked!*\n"
                            f"*Use `{global_vars.CMD_PREFIX}help fetch` for more information.*"
                        )
                    )
                ]
            ),
            user_raw_scope = scope.UserRawScope(
                path_m.DEFAULT_PATH_BUNDLE
            )
        )

        self.pats = StatisticType(
            "pat", "pats",
            server_raw_scope = scope.ServerRawScope(
                path_m.DEFAULT_PATH_BUNDLE
            ),
            user_raw_scope = scope.UserRawScope(
                path_m.DEFAULT_PATH_BUNDLE
            )
        )

        self.meows = StatisticType(
            "meow", "meows",
            server_raw_scope = scope.ServerRawScope(
                path_m.DEFAULT_PATH_BUNDLE
            ),
            user_raw_scope = scope.UserRawScope(
                path_m.DEFAULT_PATH_BUNDLE
            )
        )

        self.sticks = StatisticType(
            "stick", "sticks",
            server_raw_scope = scope.ServerRawScope(
                path_m.DEFAULT_PATH_BUNDLE
            ),
            user_raw_scope = scope.UserRawScope(
                path_m.DEFAULT_PATH_BUNDLE
            )
        )


    def get_stat_types(self) -> list[StatisticType]:
        """Gets all stat types."""
        return list(self.__dict__.values())

    def get_viewable_stat_types(self, ctx: cmds.Context):
        """Get all unlocked stat types by context."""
        return [stat_type for stat_type in self.get_stat_types() if stat_type.is_unlocked(ctx)]


    def get_stat_type(self, name: str):
        """Gets a stat type by name."""
        stat_types = self.get_stat_types()
        for stat_type in stat_types:
            if stat_type.name == name:
                return stat_type

        raise ValueError(f"Statistic type \"{name}\"not found.")


STAT_TYPES = StatisticTypes()
