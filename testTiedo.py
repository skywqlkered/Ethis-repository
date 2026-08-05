from dotenv import load_dotenv
import discord
import asyncio
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
speaker: int = 0

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user: # Prevents the bot to reply to itself
        return
    
    role: discord.Role | None = message.guild.get_role(1262396628539670538)

    if not role:
        return
    
    if role in message.author.roles:
        print("This role is staff")
    else:
        print("Role isn't staff!")
    
    if message.content.startswith("/make-speaker"):
        len_men = len(message.mentions)

        # Add functionality to the other if statements
        # Save speaker-id in the speaker variable
        # Have speaker specific commands
        if len_men == 0:
            return None
        if len_men == 1:
            user = message.mentions[0].id
            print(user)
            print(message.guild.get_role(1534534278594035853).members)
            
            await message.reply(f"{message.mentions[0].mention} you are now speaker")
            print("You are the speaker now!!!")
        if len_men >= 2:
            print("To many mentions, cant unmute more 2 people")
            return None

if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
