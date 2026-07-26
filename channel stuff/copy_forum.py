from dotenv import load_dotenv
import discord
import asyncio
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)

forum_channel_id = 1205478289762684948
new_forum_id = 1529711501466669146

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    
    if message.author.id == 398769543482179585:
        forum: discord.ForumChannel = message.guild.get_channel(forum_channel_id) # type:ignore
        tags: list[discord.ForumTag] = list(forum.available_tags) #type.ignore
        
        new_forum: discord.ForumChannel = message.guild.get_channel(new_forum_id)# type:ignore
        for tag in tags:
            
            await new_forum.create_tag(name=tag.name, emoji=tag.emoji)

        
if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
