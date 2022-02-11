"""Contains statistic types."""


import typing as typ
import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import backend.barking.path as p_b
import backend.barking.special_event as s_ev
import backend.barking.scope as sc
import backend.main_classes.str_variations as str_v
import backend.firebase.firebase_interaction as f_i


class StatisticType():
    """A class for a statistic type such as "barks" and "pats"."""
    def __init__(self, name: str, server_raw_scope: sc.ServerRawScope, user_raw_scope: sc.UserRawScope):
        self.name = name
        self.name_variations = str_v.StrVariations(name)

        def get_scope(raw_scope: sc.RawScope):
            return sc.Scope(raw_scope, name)

        self.server_scope = get_scope(server_raw_scope)
        self.user_scope = get_scope(user_raw_scope)


    async def add_stat(self, ctx: cmds.Context, amount: int):
        """Adds the amount to the stat."""
        for scope in [self.server_scope, self.user_scope]:
            await scope.add_on_scope(ctx, amount)



class StatisticTypes():
    """Contains the available statistic types."""
    def __init__(self):
        self.barks = StatisticType(
            "bark",
            server_raw_scope = sc.ServerRawScope(
                p_b.DEFAULT_PATH_BUNDLE,
                raw_special_events = [
                    s_ev.RawSpecialEvent(
                        "++pat", 2500, (
                            ">>> YAYYAYAYAYYAAYAYA- AM HAPPY!! :D!!\n"
                            "*Cani likes this server! The command `++pat` has been unlocked!*\n"
                            f"*Use `{vrs.CMD_PREFIX}help pat` for more information.*"
                        )
                    )
                ]
            ),
            user_raw_scope = sc.UserRawScope(
                p_b.DEFAULT_PATH_BUNDLE
            )
        )

        self.pats = StatisticType(
            "pat",
            server_raw_scope = sc.ServerRawScope(
                p_b.DEFAULT_PATH_BUNDLE
            ),
            user_raw_scope = sc.UserRawScope(
                p_b.DEFAULT_PATH_BUNDLE
            )
        )


    def get_stat_types(self) -> list[StatisticType]:
        """Gets all stat types."""
        return list(self.__dict__.values())

    def get_stat_type(self, name: str):
        """Gets a stat type by name."""
        stat_types = self.get_stat_types()
        for stat_type in stat_types:
            if stat_type.name == name:
                return stat_type

        raise ValueError(f"Statistic type \"{name}\"not found.")


STAT_TYPES = StatisticTypes()
