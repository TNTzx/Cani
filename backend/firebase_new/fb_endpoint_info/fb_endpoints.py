"""All Firebase endpoints."""


from .. import fb_consts
from . import fb_endpoint as endpoint


class Root(endpoint.FBEndpointRoot):
    """The root."""
    def __init__(self):
        super().__init__()

        self.e_main = self.MainData(self)
        self.e_discord = self.DiscordData(self)
        self.e_test = self.Test(self)


    class MainData(endpoint.FBEndpointParent):
        """Main variables. Used for stuff like getting the dev list."""
        def __init__(self, parent: endpoint.FBEndpoint):
            super().__init__(name = "main_data", parent = parent)

            self.e_privileges = self.Privileges(self)


        class Privileges(endpoint.FBEndpointParent):
            """Contains the privileges of each user / server."""
            def __init__(self, parent: endpoint.FBEndpoint):
                super().__init__(name = "privileges", parent = parent)

                self.e_devs = self.Devs(self)

            class Devs(endpoint.FBEndpointEnd):
                """Contains the IDs of developers."""
                def __init__(self, parent: endpoint.FBEndpoint):
                    super().__init__(name = "devs", parent = parent)


    class DiscordData(endpoint.FBEndpointParent):
        """Contains Discord-related data."""
        def __init__(self, parent: endpoint.FBEndpoint):
            super().__init__(name = "discord_data", parent = parent)

            self.e_commands = self.CommandData(self)
            self.e_guilds = self.GuildData(self)
            self.e_users_general = self.UserGeneralData(self)


        class CommandData(endpoint.FBEndpointParent):
            """Data relating to commands."""
            def __init__(self, parent: endpoint.FBEndpoint):
                super().__init__(name = "command_data", parent = parent)

                self.e_is_using = self.IsUsingCommand(self)


            class IsUsingCommand(endpoint.FBEndpointEnd):
                """Storage for the `is_using` implementation for commands."""
                def __init__(self, parent: endpoint.FBEndpoint):
                    super().__init__(name = "is_using_command", parent = parent)


        class GuildData(endpoint.FBEndpointEnd):
            """Contains guild-specific data."""
            def __init__(self, parent: endpoint.FBEndpoint):
                super().__init__(name = "guild_data", parent = parent)

            def get_default_data(self):
                return {
                    "admin_role": 0,
                    "claim_channel_data": {
                        "available_channels": [
                            fb_consts.PLACEHOLDER_DATA
                        ],
                        "embed_info": {
                            "channel_id": fb_consts.PLACEHOLDER_DATA,
                            "message_id": fb_consts.PLACEHOLDER_DATA
                        }
                    },
                    "fun": {
                        "barking": {
                            "server": fb_consts.PLACEHOLDER_DATA
                        }
                    }
                }


        class UserGeneralData(endpoint.FBEndpointParent):
            """Contains general user data, such as bans."""
            def __init__(self, parent: endpoint.FBEndpoint):
                super().__init__(name = "user_general_data", parent = parent)

                self.e_banned_users = self.BannedUsers(self)


            class BannedUsers(endpoint.FBEndpointEnd):
                """Contains a list of banned users."""
                def __init__(self, parent: endpoint.FBEndpoint):
                    super().__init__(name = "banned_users", parent = parent)


    class Test(endpoint.FBEndpointParent):
        """Used for testing."""
        def __init__(self, parent: endpoint.FBEndpoint):
            super().__init__(name = "test", parent = parent)


ENDPOINTS = Root()


class ShortEndpoint():
    """Contains shortcuts for the endpoints."""
    devs = ENDPOINTS.e_main.e_privileges.e_devs

    discord_cmds = ENDPOINTS.e_discord.e_commands
    discord_guilds = ENDPOINTS.e_discord.e_guilds
    discord_users_general = ENDPOINTS.e_discord.e_users_general

    test = ENDPOINTS.e_test
