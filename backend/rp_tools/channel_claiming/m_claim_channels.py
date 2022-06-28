"""Contains stuff about a claim channel."""


import nextcord as nx

import global_vars
import backend.firebase as firebase

from . import m_claim_excs


DEFAULT_LOCATION = "//Unknown//"


class ClaimData(firebase.FBStruct):
    """Contains claiming data for a claim channel."""
    def __init__(
            self,
            claim_status: bool = False,
            location: str = DEFAULT_LOCATION
        ):
        self.claim_status = claim_status
        self.location = location


    # TODO update this
    def firebase_to_json(self) -> list | dict:
        return {
            "claim_status": self.claim_status,
            "location": self.location
        }

    @classmethod
    def firebase_from_json(cls, json: list | dict) -> None:
        return cls(
            claim_status = json.get("claim_status"),
            location = json.get("location")
        )


class ClaimChannel(firebase.FBStruct):
    """Represents a channel that can be claimed."""
    def __init__(
            self,
            channel_id: int,
            claim_data: ClaimData = ClaimData()
        ):
        self.channel_id = channel_id
        self.claim_data = claim_data


    # TODO update this
    def firebase_to_json(self) -> list | dict:
        return {
            "channel_id": str(self.channel_id),
            "claim_status": self.claim_data.claim_status,
            "location": self.claim_data.location
        }

    @classmethod
    def firebase_from_json(cls, json: list | dict) -> None:
        return cls(
            channel_id = int(json.get("channel_id")),
            claim_data = ClaimData.firebase_from_json(json)
        )


    def discord_get_channel(self):
        """Gets the Discord channel from this object."""
        return global_vars.global_bot.get_channel(self.channel_id)


class ClaimChannels(firebase.FBStruct):
    """Contains all claim channels for a certain guild."""
    def __init__(
            self,
            claim_channels: list[ClaimChannel] = None
        ):
        if claim_channels is None:
            claim_channels = []

        self.claim_channels = claim_channels


    # TODO change name to "claim_channels"
    def firebase_to_json(self) -> list | dict:
        return [
            claim_channel.firebase_to_json() for claim_channel in self.claim_channels
        ]

    @classmethod
    def firebase_from_json(cls, json: list | dict) -> None:
        return cls(
            claim_channels = [
                ClaimChannel.firebase_from_json(claim_channel)
                for claim_channel in json
            ]
        )


    def get_claim_channel_ids(self):
        """Gets all the claimable channel IDs."""
        return [claim_channel.channel_id for claim_channel in self.claim_channels]


    def is_claimable_channel(self, channel_id: int):
        """Returns `True` if the channel is claimable, otherwise returns `False`."""
        return channel_id in self.get_claim_channel_ids()


    def get_claim_channel_by_id(self, claim_channel_id: int):
        """Gets a claim channel using ID."""
        for claim_channel in self.claim_channels:
            if claim_channel_id == claim_channel.channel_id:
                return claim_channel

        raise m_claim_excs.NoFoundClaimableChannel(claim_channel_id)


    def get_embed(self):
        """Generates an embed of all the claim channels."""
        embed = nx.Embed(title = "RP Channels", color = global_vars.DEFAULT_COLOR)

        if not len(self.claim_channels) == 0:
            for claim_channel in self.claim_channels:
                if claim_channel.claim_data.claim_status:
                    title = "Claimed"
                    description = f"`Current location:` __{claim_channel.claim_data.location}__"
                else:
                    title = "Unclaimed"
                    description = "_ _"

                channel = global_vars.global_bot.get_channel(int(claim_channel.channel_id))

                new_title = f"__#{channel.name}__: {title}"
                embed.add_field(name = new_title, value = description, inline = False)
        else:
            embed.add_field(name = "No RP channels! :(", value = f"Ask the moderators to go add one using `{global_vars.CMD_PREFIX}claimchanneledit add`.", inline = False)


        return embed
