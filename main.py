import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")

botToken = os.environ['TOKEN']
client.run(botToken)