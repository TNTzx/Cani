"""Default JSON."""

PLACEHOLDER = [["placeholder"]]


default = {
    "guilds": {
        "guildId": {
            "mainData": {
                "adminRole": "0"
            },
            "claimChannelData": {
                "availableChannels": PLACEHOLDER,
                "embedInfo": {
                    "channel": PLACEHOLDER,
                    "messageId": PLACEHOLDER
                }
            },
            "fun": {
                "barking": {
                    "users": PLACEHOLDER,
                    "totalBarks": 0,
                    "barkMilestone": 0
                }, 
            }
        }
    },
    "mainData": {
        "devs": [
            "279803094722674693"
        ]
    }
}