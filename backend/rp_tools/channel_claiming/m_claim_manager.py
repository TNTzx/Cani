"""Contains logic for managing claim channels."""


import backend.discord_utils as disc_utils
import backend.firebase as firebase

from . import m_claim_channels


def get_path_claim_channels(guild_id: int):
    """Gets the claim channel path for a guild."""
    return firebase.ShortEndpoint.discord_guilds.get_path() + [str(guild_id), "claim_channel_data"]


class ClaimChannelManager(firebase.FBStruct):
    """Manages the claim channels for a build."""
    def __init__(
            self,
            claim_channels: m_claim_channels.ClaimChannels,
            embed_pointer: disc_utils.MessagePointer
        ):
        self.claim_channels = claim_channels
        self.embed_pointer = embed_pointer


    # TODO rename to "claim_channels" and "embed_pointer"
    def firebase_to_json(self):
        return {
            "available_channels": self.claim_channels.firebase_to_json(),
            "embed_info": self.embed_pointer.firebase_to_json()
        }

    @classmethod
    def firebase_from_json(cls, json: dict | list):
        return cls(
            claim_channels = m_claim_channels.ClaimChannels.firebase_to_json(json.get("available_channels")),
            embed_pointer = disc_utils.MessagePointer.firebase_to_json(json.get("embed_info"))
        )


    @classmethod
    def from_guild_id(cls, guild_id: int):
        """Gets the claim channel manager for a guild."""
        return cls.firebase_from_json(
            firebase.get_data(get_path_claim_channels(guild_id))
        )


    def update_claim_channels(self, guild_id: int):
        """Updates the claim channel for a certain guild."""
        firebase.override_data(
            get_path_claim_channels(guild_id) + ["available_channels"],
            self.claim_channels.firebase_to_json()
        )

    def update_embed_pointer(self, guild_id: int):
        """Updates the embed pointer for a certain guild."""
        firebase.override_data(
            get_path_claim_channels(guild_id) + ["embed_info"],
            self.embed_pointer.firebase_to_json()
        )


    def update_all(self, guild_id: int):
        """Updates all claim channel data for a certain guild."""
        for func in [self.update_claim_channels, self.update_embed_pointer]:
            func(guild_id)

