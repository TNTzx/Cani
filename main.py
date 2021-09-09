import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")

client.run(os.getenv("TOKEN"))