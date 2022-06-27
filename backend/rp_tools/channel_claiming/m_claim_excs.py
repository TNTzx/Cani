"""Contains all exceptions for channel claiming."""


class ChannelClaimException(Exception):
    """
    Exception.
    A channel claiming exception has occured.
    """


class NoFoundClaimableChannel(ChannelClaimException):
    """
    Exception.
    A claimable channel cannot be found.
    """
    def __init__(self, failed_channel_id: int):
        super().__init__(f"No claim channel found with given ID: {failed_channel_id}")


class MissingEmbed(ChannelClaimException):
    """
    Exception.
    There is no set up claim channel embed for this guild, or the bot can't find any.
    """
