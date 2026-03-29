from dotenv import load_dotenv
import discord
import asyncio
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

async def main():
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    if TOKEN:
        await client.start(TOKEN)
    else:
        raise ReferenceError("TOKEN doesnt exist")

asyncio.run(main())