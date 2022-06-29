"""Variables."""


import nextcord as nx


# Bot
global_bot = nx.Client()

# tent
tntz: nx.User = None

# Command Prefix
CMD_PREFIX = "++"


class Timeouts:
    """Class that contains common timeout durations."""
    short = 10
    medium = 60
    long = 60 * 10


DEFAULT_COLOR = 0x5865F2
