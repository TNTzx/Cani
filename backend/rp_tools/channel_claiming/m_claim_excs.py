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


class AlreadyClaimableChannel(ChannelClaimException):
    """
    Exception.
    The channel is already claimable.
    """
    def __init__(self, channel_id: int):
        super().__init__(f"Channel ID {channel_id} is already claimable.")

class AlreadyNotClaimableChannel(ChannelClaimException):
    """
    Exception.
    The channel is already not claimable.
    """
    def __init__(self, channel_id: int):
        super().__init__(f"Channel ID {channel_id} is already not claimable.")


class OrderListNotMatching(ChannelClaimException):
    """
    Exception.
    The list of channel IDs doesn't match with the list of claim channel IDs.
    """
