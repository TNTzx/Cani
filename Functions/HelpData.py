import main
from Functions import FirebaseInteraction as fi


def helpData(ctx):
    x = {
        "Channel Claiming": {
            "claimchannel": {
                "description": "Claims / unclaims the current RP channel to a specific location.",
                "parameters": {
                    "[claim | unclaim]": "Tells if you want to claim or unclaim the current RP channel.",
                    "location": "The location of where you want the channel to be in. Surround the location with quotes (example: `\"Imagination Room\"`).\nNote that __this parameter doesn't have to be filled in when you're `unclaim`ing__ the channel."
                },
                "aliases": [
                    "cc"
                ],
                "cooldown": 60 * 2,
                "exampleUsage": [
                    f"{main.commandPrefix}claimchannel claim \"Quaz's HQ\"",
                    f"{main.commandPrefix}claimchannel unclaim"
                ]
            },
            "claimchanneledit": {
                "description": "Adds / removes the channel as an RP channel.",
                "parameters": {
                    "[add | remove]": "Tells if you want to add or remove a channel as an RP channel.",
                    "channel": "Channel that you want to add / remove as an RP channel."
                },
                "requireAdminRole": True,
                "aliases": [
                    "cce"
                ],
                "exampleUsage": [
                    f"{main.commandPrefix}claimchanneledit add #general-rp-1",
                    f"{main.commandPrefix}claimchanneledit remove #general-rp-1"
                ]
            },
            "claimchannelembed": {
                "description": "Changes where the embed for displaying claimed channels are sent.",
                "parameters": {
                    "channel": "Channel where the embed will be put in."
                },
                "requireAdminRole": True,
                "aliases": [
                    "ccm"
                ],
                "exampleUsage": [
                    f"{main.commandPrefix}claimchannelembed #general-display"
                ]
            },
            "claimchannelupdate": {
                "description": "Updates the embed for displaying claimed channels.",
                "requireAdminRole": True,
                "aliases": [
                    "ccu"
                ]
            }
        },

        "Bot Control": {
            "switchkill": {
                "description": "Shuts the bot down.",
                "requireAdminRole": True,
                "aliases": [
                    "sk"
                ]
            },
            "switchrestart": {
                "description": "Restarts the bot.",
                "requireAdminRole": True,
                "aliases": [
                    "sr"
                ]
            },
            "updatedatabase": {
                "description": "Updates the database for new guilds.",
                "requireAdminRole": True,
                "aliases": [
                    "ud"
                ]
            }
        },

        "Basic Commands": {
            "hello": {
                "description": "Sends a hello message! :D"
            },
            "ping": {
                "description": "I ping you back! :D"
            },
            "help": {
                "description": "HOW THE HECK DID YOU GET HERE IF YOU'VE- WHAT- OH MY GOODNESS WHY- WHY DID YOU DO THIS-",
                "parameters": {
                    "[command]": "WHY DID YOU GET HELP FOR A HELP COMMAND ARE YOU I N S A N E"
                },
                "aliases": [
                    "h"
                ]
            }
        },
        "Barking": {
            "bark": {
                "description": "BARK",
                "aliases": [
                    "b"
                ],
                "cooldown": 2
            },
            "barkrank": {
                "description": "Displays barking leaderboards along with the total bark count! ~~WHY DID I DO THIS~~",
                "aliases": [
                    "br"
                ],
                "cooldown": 60 * 2
            },
            "pat": {
                "description": "PATPATPATPTPATAPTPATPPA (More borks!)",
                "aliases": [
                    "pt"
                ],
                "cooldown": 1 * 60 * 60 * 12,
                "showCondition": lambda: fi.getData(["guilds", ctx.guild.id, "fun", "barking", "barkMilestone"]) == 10000
            }
        },

        "Fun": {
            "meow": {
                "description": "No. No. Please don't."
            },
            "pork": {
                "description": "Pork. That's it. That's all you get. Pork."
            }
        }
    }

    return x