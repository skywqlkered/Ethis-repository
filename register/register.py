from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext.commands import has_role
from functions import get_json_item, get_username, get_uuid, add_entry, backup_registry, edit_entry, remove_entry
import os

support_ticket_channel_id = 926102810930589726

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

async def send_entry_log(entries: list[dict], action: str):
    log_channel = client.get_channel(1419741195424366612)
    if isinstance(log_channel, discord.TextChannel):
        if len(entries) == 1:
            await log_channel.send(action + ": " + str(entries[0]))
        else:
            old_entry = entries[0]
            new_entry = entries[1]
            await log_channel.send(action + ": " + "\n\tOld entry:"+str(entries[0]) + "\n\tNew entry:"+str(entries[1]))
            

@client.event
async def on_ready():
    server_id = 925805443887022121
    tree.copy_global_to(guild=discord.Object(id=server_id))
    synced_commands = await tree.sync(
        guild=discord.Object(id=server_id)
    )  # ethis
    print(
        f"I have logged in as {client.user} and synced {len(synced_commands)} commands."
    )

@tree.command(description="Registers yourself for the whitelist")
@app_commands.default_permissions(priority_speaker=True)
@app_commands.describe(username="Your Minecraft username")
async def register(interaction: discord.Interaction, username: str):
    if get_json_item("discord_id", interaction.user.id):
        await interaction.response.send_message("You have already registered a Minecraft username, if you want to register a different one: use /edit-registration.", ephemeral=True)
        return
    
    if get_json_item("mc_username", username):
        await interaction.response.send_message(f"Someone has already registered this username, if this is your name: please make a support ticket in <#{support_ticket_channel_id}>.", ephemeral=True)
        return

    uuid = get_uuid(username)
    if not uuid:
        await interaction.response.send_message(f"Minecraft username not found, please try again. If you are _very_ sure this username exists, please make a support ticket in <#{support_ticket_channel_id}>.", ephemeral=True)
        return
    if uuid:
        corrected_username = get_username(uuid) #type: ignore
        if corrected_username:
            username = corrected_username
            
    backup_registry()
    entry = add_entry(discord_id=interaction.user.id, uuid=uuid, username=username)
    if interaction.guild and isinstance(interaction.user, discord.Member):
        whitelist_role = interaction.guild.get_role(1511480573485383963)
        if whitelist_role:
            await interaction.user.add_roles(whitelist_role, reason="Added to the whitelist")
            
    await send_entry_log([entry], "Add")
    await interaction.response.send_message(f"Connected <@{entry["discord_id"]}> to Minecraft username {entry["mc_username"]}", ephemeral=True)

@tree.command(name="edit-registration", description="Edits your registration for the whitelist")
@app_commands.default_permissions(priority_speaker=True)
@app_commands.describe(username="Your Minecraft username")
async def edit_register(interaction: discord.Interaction, username: str):
    if get_json_item("mc_username", username):
        await interaction.response.send_message(f"Someone has already registered this username, if this is your name: please make a support ticket in <#{support_ticket_channel_id}>.", ephemeral=True)
        return

    uuid = get_uuid(username)
    if not uuid:
        await interaction.response.send_message(f"Minecraft username not found, please try again. If you are _very_ sure this username exists, please make a support ticket in <#{support_ticket_channel_id}>.", ephemeral=True)
        return
    if uuid:
        corrected_username = get_username(uuid) #type: ignore
        if corrected_username:
            username = corrected_username
            
    backup_registry()
    entries = edit_entry(discord_id=interaction.user.id, uuid=uuid, username=username)
    await send_entry_log(entries, "Edit")#type:ignore
    if entries:
        entry = entries[1]
        await interaction.response.send_message(f"Connected <@{entry["discord_id"]}> to Minecraft username **{entry["mc_username"]}**", ephemeral=True) #type:ignore
    else:
        await interaction.response.send_message(f"idk what happened here, ask sky, {entries}", ephemeral=False) #type:ignore


@client.event
async def on_raw_member_remove(payload: discord.RawMemberRemoveEvent):
    user_id = payload.user.id
    entry = remove_entry(user_id)
    if entry:
        await send_entry_log([entry], "Server Leave")

#bottom of the page
@tree.error # type:ignore
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(
            "You don't have permission to use this command.",
            ephemeral=True
        )
        return

    # Log unexpected errors
    print(f"Unhandled command error: {error}")

if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
