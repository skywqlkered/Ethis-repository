from dotenv import load_dotenv
import discord
import asyncio
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)

async def give_speaker_role(message: discord.Message):
    speaker_role: list = message.guild.get_role(1534534278594035853)

    selected_member: discord.Member = message.mentions[0]
    print(f"User uit mention: {selected_member}")
    
    await selected_member.add_roles(speaker_role)

async def remove_speaker_roles(message: discord.Message):
    speaker_role: list = message.guild.get_role(1534534278594035853)

    selected_member: discord.Member = message.mentions[0]
    print(f"User uit mention: {selected_member}")
    
    await selected_member.remove_roles(speaker_role)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user: # Prevents the bot to reply to itself
        return
    
    presentation_role: discord.Role | None = message.guild.get_role(1262396628539670538)

    if not presentation_role:
        return
    
    if message.content.startswith("/roles"):
        get_role_names: list = message.guild.get_role(1534534278594035853).members

        await message.reply(f"Deze mensen hebben de presentatie rol: {get_role_names}")

    if message.content.startswith("/make-speaker"):
        len_men = len(message.mentions)

        if len_men == 1:
            await give_speaker_role(message)
            await message.reply(f"{message.mentions[0].mention} you are now speaker")
        else:
            await message.reply("Please only select one person")
            return None

    if message.content.startswith("/remove-speaker"):
        await remove_speaker_roles(message)
        await message.reply("Removed \"Speaker-Role\" from all Users")

if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
