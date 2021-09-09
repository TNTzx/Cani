import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("//"):
        messageCut = message[2:]

        if messageCut == "hello":
            await message.channel.send("*Bark!*")

botToken = os.environ['TOKEN']
client.run(botToken)