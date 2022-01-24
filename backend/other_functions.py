"""Other fun functions!"""

# pylint: disable=line-too-long
# pylint: disable=unused-argument
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods


import asyncio
import datetime
import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import backend.exceptions.custom_exc as c_exc


class DataStructure:
    """Parent class where data structures are inherited in."""
    def get_dict(self):
        """Gets dictionary of stored data."""
        return get_dict_attr(self)

class Match:
    """Structure that contains a dictionary and a value to match it with."""
    def __init__(self, data_dict: dict[object, str], value: object):
        self.data_dict = data_dict
        self.value = value

    def get_name(self):
        """Gets the name of the value."""
        return self.data_dict[self.value]

class Unique():
    """Unique variable!"""
    def __init__(self):
        pass

class MessagePointer(DataStructure):
    """Class that contains channel and message ids to represent a message."""
    def __init__(self, datas: dict = None, channel_id = "0", message_id = "0"):
        if datas is None:
            datas = {
                "channel_id": channel_id,
                "message_id": message_id
            }
        self.channel_id = str(datas["channel_id"])
        self.message_id = str(datas["message_id"])

    async def get_message(self):
        """Gets the message from discord and returns it."""
        channel: nx.TextChannel = vrs.global_bot.get_channel(int(self.channel_id))
        if channel is None:
            return None
        message: nx.Message = await channel.fetch_message(int(self.message_id))
        if message is None:
            return None

        return message

async def get_tntz():
    """Gets TNTz."""
    return await vrs.global_bot.fetch_user(279803094722674693)


def format_time(num: int):
    """Formats the time from seconds to '#h #m #s'."""
    seconds = num
    time = str(datetime.timedelta(seconds=seconds))
    time = time.split(":")

    time_final_list = []
    if not time[0] == "0":
        time_final_list.append(f"{int(time[0])}h")
    if not time[1] == "00":
        time_final_list.append(f"{int(time[1])}m")
    if not time[2] == "00":
        time_final_list.append(f"{int(time[2])}s")

    time_final = " ".join(time_final_list)
    if time_final == "":
        time_final = "less than a second"
    return time_final


async def get_channel_from_mention(mention: str):
    """Gets channel from a mention."""
    get_id = mention[2:-1]
    obj = vrs.global_bot.get_channel(int(get_id))
    return obj


def get_dict_attr(obj):
    """Gets attributes of an object then returns it as a dict."""
    def check_if_has_dict(obj):
        return hasattr(obj, "__dict__")

    dictionary = {}
    for attr, value in obj.__dict__.items():
        if isinstance(value, list):
            value_list = []
            for value_item in value:
                if not check_if_has_dict(value_item):
                    value_list.append(value_item)
                else:
                    value_list.append(get_dict_attr(value_item))
            dictionary[attr] = value_list
        elif not check_if_has_dict(value):
            dictionary[attr] = value
        else:
            dictionary[attr] = get_dict_attr(value)
    return dictionary


def override_dicts_recursive(default: dict, override: dict):
    """Override values of a dict with another dict."""
    new = default.copy()
    for key in override.keys():
        if key in default:
            if isinstance(default[key], dict) and isinstance(override[key], dict):
                new[key] = override_dicts_recursive(default[key], override[key])
            else:
                new[key] = override[key]
        else:
            raise c_exc.DictOverrideError(f"Key '{key}' on override dict doesn't have an entry in default dict.")

    return new

def is_not_blank_str(string: str | None):
    """Checks if a string is blank or None."""
    if string is None:
        return False
    if string.strip() == "":
        return False
    return True

def remove_none_in_list(_list: list):
    """Removes all instances of None in a list."""
    clean_list = []
    for item in _list:
        if item is None:
            continue
        clean_list.append(item)
    return clean_list

def subtract_list(minuend: list, subtrahend: list):
    """Subtracts lists."""
    return [item for item in minuend if item not in subtrahend]

async def delay_message(ctx: cmds.Context, text: str, duration: int = 2, delete=False):
    """Delays the message."""
    message = await ctx.send(text)
    await asyncio.sleep(duration)

    if delete:
        await message.delete()
    else:
        return message