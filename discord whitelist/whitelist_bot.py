import os

import discord
from command_utils import add_user_to_whitelist
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    ethis_id = 925805443887022121
    # test3_id = 987779478413525023
    current_id = ethis_id
    tree.copy_global_to(guild=discord.Object(id=current_id))
    # ethis
    synced_commands = await tree.sync(guild=discord.Object(id=current_id))
    print(
        f"I have logged in as {client.user} and synced {len(synced_commands)} commands.")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return


async def log_username(interaction: discord.Interaction, name: str):
    channel = interaction.guild.get_channel(  # type: ignore
        1419741195424366612)
    await channel.send(name)  # type: ignore


@tree.command(name="whitelist-add", description="Adds a user to the whitelist")
@app_commands.default_permissions(bypass_slowmode=True)
@app_commands.describe(name="The name of the player you're adding.")
async def texture(interaction: discord.Interaction, name: str):
    response = add_user_to_whitelist(name)

    await interaction.response.send_message(response, ephemeral=True)
    await log_username(interaction, name)

if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
