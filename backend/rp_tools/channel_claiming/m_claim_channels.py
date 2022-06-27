"""Contains stuff about a claim channel."""


import global_vars
import backend.other as other


DEFAULT_LOCATION = "Unknown"


class ClaimChannel(other.JSONInterface):
    """Represents a channel that can be claimed."""
    def __init__(
            self,
            channel_id: int,
            claim_status: bool = False,
            location: str = DEFAULT_LOCATION
        ):
        self.channel_id = channel_id
        self.claim_status = claim_status
        self.location = location


    def to_json(self) -> list | dict:
        return {
            "channel_id": str(self.channel_id),
            "claim_status": self.claim_status,
            "location": self.location
        }

    @classmethod
    def from_json(cls, json: list | dict) -> None:
        return cls(
            channel_id = int(json.get("channel_id")),
            claim_status = json.get("claim_status"),
            location = json.get("location")
        )


    def discord_get_channel(self):
        """Gets the Discord channel from this object."""
        return global_vars.global_bot.get_channel(self.channel_id)


class ClaimChannels(other.JSONInterface):
    """Contains all claim channels for a certain guild."""
    def __init__(
            self,
            claim_channels: list[ClaimChannel] = None
        ):
        if claim_channels is None:
            claim_channels = []

        self.claim_channels = claim_channels


    # TODO change name to "claim_channels"
    def to_json(self) -> list | dict:
        return {
            "available_channels": [
                claim_channel.to_json() for claim_channel in self.claim_channels
            ]
        }

    @classmethod
    def from_json(cls, json: list | dict) -> None:
        return cls(
            claim_channels = json.get("available_channels")
        )
