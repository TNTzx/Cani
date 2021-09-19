import json

helpDict = {
        "Channel Claiming": {
            "claimchannel": {
                "description": "Claims the current RP channel to a specific location.",
                "parameters": {
                    "location": "The location of where you want the channel to be in. Surround the location with quotes (example: `\"Imagination Room\"`)."
                }
            },
            "unclaimchannel": {
                "description": "Unclaims the RP channel."
            },
            "editclaimchannels":{
                "description": "Adds / removes the channel as an RP channel.",
                "parameters": {
                    "add | remove": "Tells if you want to add or remove a channel as an RP channel.",
                    "channel": "Channel that you want to add / remove as an RP channel."
                },
                "requireAdminRole": True
            }
        },
        "Bot Control": {
            "killswitch": {
                "description": "Shuts the bot down.",
                "requireAdminRole": True
            },
            "restartswitch": {
                "description": "Restarts the bot.",
                "requireAdminRole": True
            }
        },
        "Fun": {
            "hello": {
                "description": "Sends a hello message! :D"
            },
            "ping": {
                "description": "I ping you back! :D"
            },
            "bark": {
                "description": "...why do you need help for a.. bark command..?"
            }
        }
    }

def getCommand(command):
    for category, commands in helpDict.items():
        if command in commands:
            return helpDict[category][command]
    return None

print(getCommand("claimchannel"))
