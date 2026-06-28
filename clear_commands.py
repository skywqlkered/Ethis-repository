import discord
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    guilds = [guild.id for guild in client.guilds]
    print(f'The {client.user.name} bot is in {len(guilds)} Guilds.\nThe guilds IDs list: {guilds}') # type:ignore
    for guildId in guilds:
        guild = discord.Object(id=guildId)
        print(f'Deleting commands from {guildId}.....')
        tree.clear_commands(guild=guild,type=None)
        await tree.sync(guild=guild)
        print(f'Deleted commands from {guildId}!')
        continue
    print('Deleting global commands.....')
    tree.clear_commands(guild=None,type=None)
    await tree.sync(guild=None)
    print('Deleted global commands!')
    exit()

client.run(DISCORD_TOKEN)