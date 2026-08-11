from dotenv import load_dotenv
import discord
import asyncio
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.type.value == 18 and message.channel.id == 1533849102960558141: # 18 = discord.MessageType.thread_created, # 1533849102960558141 = gamenight ideas
        await message.delete()
    

if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
