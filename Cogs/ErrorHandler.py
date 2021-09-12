import discord
from discord.ext import commands
import os
import asyncio
import main
import sys
import traceback
import datetime

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):

        if isinstance(exc, commands.CommandOnCooldown):
            numberOfSeconds = int(str(round(exc.retry_after, 0))[:-2])
            timeConverted = str(datetime.timedelta(seconds=numberOfSeconds))
            timeSplit = timeConverted.split(":")
            timeFormatted = f"`{timeSplit[0]}h {timeSplit[1]}m {timeSplit[2]}s`"

            await ctx.send(f"*Error! D:\nThe command is on cooldown for {timeFormatted} more! >:(*")
            return
        
        if isinstance(exc, commands.MissingRole):
            await ctx.send(f"*Error! D:*\n*You don't have the `{exc.missing_role}` role! >:(*")
            return

        error = getattr(exc, 'original', exc)

        print(f"Ignoring exception in command {ctx.command}:")
        traceback.print_exception(type(error), error, error.__traceback__)

        await ctx.send(f"*Error! D:* ```{error}```")

        tntz = await main.bot.fetch_user(279803094722674693)
        await tntz.send(f"*Error in `{ctx.guild.name}`! D:*\n*Link: *`{ctx.message.jump_url}`\n```{error}```")

def setup(bot):
    bot.add_cog(ErrorHandler(bot))