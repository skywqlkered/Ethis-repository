from dotenv import load_dotenv
import discord
import asyncio
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)

category_ids = [926090651840442409, 925805443887022122, 1475927265555648566, 1482000287508987934]

id_everyone = 925805443887022121
id_ethizian = 925808103436455936
id_testrole = 1491116744880951316
id_inactive = 1271867768240734312

override_everyone:discord.PermissionOverwrite = discord.PermissionOverwrite()
override_everyone.read_message_history = True
override_everyone.read_messages = True
override_everyone.send_messages = False
override_everyone.send_messages_in_threads = False
override_everyone.send_polls = False
override_everyone.send_tts_messages = False
override_everyone.send_voice_messages = False

async def set_channel_permission(guild: discord.Guild):
    role: discord.Role | None = guild.get_role(id_everyone)
    for id in category_ids:
        channel = guild.get_channel(id)
        
        if isinstance(channel, discord.CategoryChannel):
            category: discord.CategoryChannel = channel
            for channel in category.channels:
                if channel.id in [926102810930589726, 1482000660844249210, 1482000317024567327]:
                    continue
                await channel.set_permissions(role, overwrite=override_everyone)
    
        
        

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    guild:discord.Guild | None = message.guild
    if guild:
        await message.channel.send("permission changing started.")
        await set_channel_permission(guild)
        await message.channel.send("Channel permissions set")
        
        
if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
