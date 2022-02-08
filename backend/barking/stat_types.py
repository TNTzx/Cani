"""Types of statistics."""


import nextcord as nx
import nextcord.ext.commands as cmds

import backend.main_classes.str_variations as s_v


class BarkingStat():
    """Defines a barking statistic."""
    def __init__(self, name_singular: str, name_plural: str, path_guild_total: str, path_user_total: str):
        self.name_singular = s_v.StrVariations(name_singular)
        self.name_plural = s_v.StrVariations(name_plural)
        self.path_guild_total = path_guild_total
        self.path_user_total = path_user_total

    def add_to_stat(self, ctx: cmds.Context, amount: int):
        """Adds a value to the statistic."""


class BarkingStats():
    """Contains barking statistics."""
    bark = BarkingStat("bark", "barks", "totalBarks", "barkCount")
