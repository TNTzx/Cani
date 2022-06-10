"""Variables."""

import json
import os
import pyrebase

import nextcord as nx


# Bot
global_bot = nx.Client()

# tent
tntz: nx.User = None

# Command Prefix
CMD_PREFIX = "++"
