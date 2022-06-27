"""Contains logic for managing claim channels."""


import backend.discord_utils as disc_utils
import backend.firebase as firebase

from . import m_claim_channels


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
            claim_channels = m_claim_channels.ClaimChannels.firebase_to_json(json.get("claim_channels")),
            embed_pointer = disc_utils.MessagePointer.firebase_to_json(json.get("embed_info"))
        )
