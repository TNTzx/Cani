import discord
from discord.ext import commands
import os
import asyncio
import main
import sys

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        await ctx.send(f"*Error! D:* ```{exc}```")

def setup(bot):
    bot.add_cog(ErrorHandler(bot))