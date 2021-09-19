import discord
from discord.ext import commands
import os
import asyncio

import main
from Functions import sqlInteraction as sI
from Functions import customExceptions as cE

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}.")

        for guild in main.bot.guilds:
            get = sI.getData(guild.id, "claim_channel_data")
            if get == None:
                sI.createData(guild.id)
            if get == "nodata":
                sI.editData(guild.id, claim_channel_data={}, claim_channel_embed={})

    @commands.command()
    async def hello(self, ctx):
        Hello.barkCount += 1
        await ctx.send(f"*Bark! I'm an actual bot! :D*")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"*Pong! <@{ctx.author.id}> :D*")

    barkCount = 0

    @commands.command()
    async def bark(self, ctx):
        self.barkCount += 1
        await ctx.send(f"*Bark! :D*\nI've barked for a total of {self.barkCount} times!")

def setup(bot):
    bot.add_cog(Hello(bot))



