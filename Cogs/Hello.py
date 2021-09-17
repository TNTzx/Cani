import discord
from discord.ext import commands
import os
import asyncio

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}.")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"*Bark! I'm an actual bot! :D*")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"*Pong! <@{ctx.author.id}> :D*")

    @commands.command()
    async def bark(self, ctx):
        await ctx.send(f"*Bark! :D*")

def setup(bot):
    bot.add_cog(Hello(bot))



