"""Contains logic for managing claim channels."""


import nextcord as nx
import nextcord.ext.commands as nx_cmds

import backend.discord_utils as disc_utils
import backend.firebase as firebase
import backend.exc_utils as exc_utils

from . import m_claim_channels
from . import m_claim_excs


def get_path_claim_channels(guild_id: int):
    """Gets the claim channel path for a guild."""
    return firebase.ShortEndpoint.discord_guilds.get_path() + [str(guild_id), "claim_channel_data"]


class ClaimChannelManager(firebase.FBStruct):
    """Manages the claim channels for a build."""
    def __init__(
            self,
            claim_channels: m_claim_channels.ClaimChannels = m_claim_channels.ClaimChannels(),
            embed_pointer: disc_utils.MessagePointer = disc_utils.MessagePointer()
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
            claim_channels = m_claim_channels.ClaimChannels.firebase_from_json(json.get("available_channels", m_claim_channels.ClaimChannels().firebase_to_json())),
            embed_pointer = disc_utils.MessagePointer.firebase_from_json(json.get("embed_info", disc_utils.MessagePointer().firebase_to_json()))
        )


    @classmethod
    def from_guild_id(cls, guild_id: int):
        """Gets the claim channel manager for a guild."""
        return cls.firebase_from_json(
            firebase.get_data(
                get_path_claim_channels(guild_id),
                default = cls().firebase_to_json()
            )
        )


    async def update_embed(self):
        """Updates the embed for the embed pointer."""
        message = await self.embed_pointer.get_message()
        if message is None:
            raise m_claim_excs.MissingEmbed()

        await message.edit(embed = self.claim_channels.get_embed())

    async def update_embed_safe(self, ctx: nx_cmds.Context):
        """Updates the embed, but with protection to missing embeds for a guild by sending an error to `ctx`."""
        try:
            await self.update_embed()
        except m_claim_excs.MissingEmbed:
            await exc_utils.SendWarn(
                error_place = exc_utils.ErrorPlace.from_context(ctx),
                suffix = "There is no set up embed for this server, or the message for it has been deleted! Use `++claimchannelembed` to set it up!"
            ).send()


    async def update_claim_channels(self, guild_id: int):
        """Updates the claim channel for a certain guild."""
        claim_channels_json = self.claim_channels.firebase_to_json()
        path = get_path_claim_channels(guild_id) + ["available_channels"]

        if len(claim_channels_json) == 0:
            firebase.delete_data(path)
        else:
            firebase.override_data(path, claim_channels_json)


    def update_embed_pointer(self, guild_id: int):
        """Updates the embed pointer for a certain guild."""
        firebase.override_data(
            get_path_claim_channels(guild_id) + ["embed_info"],
            self.embed_pointer.firebase_to_json()
        )

    async def set_embed(self, guild_id: int, channel: nx.TextChannel):
        """Sets the embed for this server."""
        message = await channel.send(embed = self.claim_channels.get_embed())
        self.embed_pointer = disc_utils.MessagePointer.from_message(message)
        self.update_embed_pointer(guild_id)


    async def update_all(self, guild_id: int):
        """Updates all claim channel data for a certain guild."""
        for func in [self.update_claim_channels, self.update_embed_pointer]:
            func(guild_id)
