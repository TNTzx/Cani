"""Other fun functions!"""


import math
import asyncio
import datetime
import nextcord.ext.commands as cmds

import global_vars


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
    obj = global_vars.global_bot.get_channel(int(get_id))
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

def is_not_blank_str(string: str | None):
    """Checks if a string is blank or None."""
    if string is None:
        return False
    if string.strip() == "":
        return False
    return True

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

def pr_print(value, tab_ch = '\t', newline_char = '\n', indent = 0):
    """Returns a string for pretty logging."""
    prefix_char = newline_char + tab_ch * (indent + 1)
    if isinstance(value, dict):
        items = [
            prefix_char + repr(key) + ": " + pr_print(value[key], tab_ch, newline_char, indent + 1)
            for key in value
        ]
        return ",".join(items) + newline_char + tab_ch * indent
    if isinstance(value, (list, tuple)):
        items = [
            prefix_char + pr_print(item, tab_ch, newline_char, indent + 1)
            for item in value
        ]
        return ",".join(items) + newline_char + tab_ch * indent

    return repr(value)


def get_page(_list: list, page: int, page_length: int):
    """Gets the page of a list. `page` is zero-indexed. Make sure list is ordered. Returns the list with the page."""
    left = page_length * page
    right = left + page_length

    if right > len(_list):
        new_list = _list[left:]
    new_list = _list[left : right]

    if len(new_list) == 0:
        raise IndexError(f"Page {page} with page length {page_length} exceeded for list of length {len(_list)} (trying to find left mark at index {left})")

    return new_list

def get_page_dict(_dict: dict, page: int, page_length: int):
    """Same as `get_page`, but with a dictionary."""
    keys_paged = get_page(list(_dict.keys()), page, page_length)
    return {key: _dict[key] for key in keys_paged}

def page_amount(_list: list, page_length: int):
    """Gets the amount of pages available for the list."""
    return math.ceil(len(_list) / page_length)


def sort_dict_with_func(_dict: dict, func, reverse = False):
    """Sorts a dictionary using a function.
    Function must take one argument in which the value of a key is put into."""

    sorted_keys = sorted(_dict, key=lambda key: func(_dict[key]), reverse=reverse)

    sorted_dict = {key: _dict[key] for key in sorted_keys}

    return sorted_dict
