"""Contains the backend for channel claiming."""


import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars.variables as vrs
import global_vars.defaultstuff as df
import backend.exceptions.send_error as s_e
import backend.exceptions.custom_exc as c_e
import backend.firebase.firebase_interaction as f_i


async def get_fb_path(ctx: cmds.Context):
    """Gets the firebase path from the context."""
    return ["guilds", str(ctx.guild.id), "claimChannelData"]


async def get_channels(ctx: cmds.Context):
    """Gets all available claim channels."""
    path = await get_fb_path(ctx)
    data = f_i.get_data(path + ["availableChannels"])
    if data == "null":
        f_i.override_data(path + ["availableChannels"], df.PLACEHOLDER)
        return {}
    if not data == df.PLACEHOLDER:
        return {
            channel["channelId"]: {
                "claimStatus": channel["claimStatus"],
                "location": channel["location"]
                }
            for channel in data}

    return {}

async def edit_claims(ctx: cmds.Context, data: dict[int, dict[str, bool | str]]):
    """Edits the claim."""
    path = await get_fb_path(ctx)
    new_data = [{
        "channelId": str(channel_id),
        "claimStatus": channel_data["claimStatus"],
        "location": channel_data["location"]
    } for channel_id, channel_data in data.items()]
    f_i.override_data(path + ["availableChannels"], new_data)


async def is_rp_channel( ctx: cmds.Context):
    """Checks if the channel is claimable or not."""
    channels = await get_channels(ctx)
    return str(ctx.channel.id) in channels.keys()


async def edit_channel_database(ctx: cmds.Context, claim_status, place, *dump):
    """Edits the channel database."""
    if len(place) >= 200:
        await s_e.send_error(ctx, "*You can't have locations with more than 200 characters! >:(*")
        raise c_e.ExitFunction()

    channels = await get_channels(ctx)
    channels[str(ctx.channel.id)]["claimStatus"] = claim_status
    channels[str(ctx.channel.id)]["location"] = place
    await edit_claims(ctx, channels)


async def update_embed(ctx: cmds.Context):
    """Updates the embed."""
    path = await get_fb_path(ctx)
    claim_channels = await get_channels(ctx)

    embed = nx.Embed(title="RP Channels", color=0x0000ff)

    if not len(claim_channels) == 0:
        for channel_id, data in claim_channels.items():
            if data["claimStatus"]:
                title = "Claimed"
                description = f"`Current location:` __{data['location']}__"
            else:
                title = "Unclaimed"
                description = "_ _"

            channel = vrs.global_bot.get_channel(int(channel_id))

            new_title = f"__#{channel.name}__: {title}"
            embed.add_field(name=new_title, value=description, inline=False)
    else:
        embed.add_field(name="No RP channels! :(", value=f"Ask the moderators to go add one using `{vrs.CMD_PREFIX}claimchanneledit add`.", inline=False)

    embed_info = f_i.get_data(path +  ["embedInfo"])
    if embed_info["channel"] == df.PLACEHOLDER:
        await s_e.send_error(ctx, "*There hasn't been a channel added to display claimed channels. Please ask the moderators / admins to add one!*")
        return

    embed_channel = vrs.global_bot.get_channel(int(embed_info["channel"]))
    embed_message = await embed_channel.fetch_message(int(embed_info["messageId"]))

    await embed_message.edit(embed=embed)
