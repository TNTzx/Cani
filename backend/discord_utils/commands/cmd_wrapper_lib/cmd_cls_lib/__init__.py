"""Library that contains the command class."""


from .cmd_cls import DiscordCommand

from .cmd_categories import \
    CmdCategory, \
        CategoryChannelClaiming, CategoryBarking, CategoryFun, \
        CategoryBasics, CategoryBotControl, CategoryModeration

from .cmd_exts import \
    CmdInfo, \
        CooldownInfo, UsabilityInfo

from .cmd_perms import \
    Permission, Permissions, \
    PermNotBanned, PermDev, PermGuildAdmin, PermGuildOwner
