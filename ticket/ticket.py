from dotenv import load_dotenv
import discord
import os
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


person_questions = """
**What would you like us to call you and what are your pronouns?**
``                             ``

**Will you be using the in game voice chat?**
``                                  ``

**How old are you?**
``             ``

**Which timezone do you live in?**
``                         ``

"""


welcome_message = """
A <@&1261617495954034698> member will look at your ticket, please have patience!

```
**What do you enjoy doing in Minecraft?**


**What has been your experience playing on Minecraft servers or SMPs?**


**Tell us more about yourself! Share your hobbies, a fun fact, or anything else you'd like us to know!**


**Ethis hosts many types of events. If you were to host your own, what would it look like?**
``` 


"""

def setup_embed_personal() -> discord.Embed:
    embed: discord.Embed = discord.Embed(color=discord.Color.from_rgb(115, 115, 115))
    embed.add_field(name='', value=person_questions, inline=True)
    return embed

def setup_embed_welcom() -> discord.Embed:
    embed: discord.Embed = discord.Embed(color=discord.Color.from_rgb(216, 107, 44))
    embed.add_field(name='Please also answer the questions below:', value=welcome_message, inline=True)
    return embed


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.content.startswith('/send form') and 1261617495954034698 in [role.id for role in message.author.roles]: #type: ignore
        try:
            await message.channel.send(embed=setup_embed_personal())
            await message.channel.send(embed=setup_embed_welcom())
            await message.delete()
        except Exception as errorman:
            await message.guild.get_channel(1419741195424366612).send(str(errorman)) # type: ignore

@client.event
async def on_guild_channel_create(channel: discord.abc.GuildChannel):
    if channel.category is None:
        return
    if channel.category.id == 1226215408126791832 and channel.name.startswith('ticket') and isinstance(channel, discord.TextChannel):
        try:
            def check(message):
                return message.channel == channel

            await client.wait_for('message', check=check)
            await channel.send(embed=setup_embed_personal())
            await channel.send(embed=setup_embed_welcom())
        except Exception as errorman:
            await channel.guild.get_channel(1419741195424366612).send(str(errorman)) #type: ignore

@client.event
async def on_guild_channel_update(before, after: discord.abc.GuildChannel):
    if isinstance(after, discord.TextChannel):
        if after.name.startswith('closed') and isinstance(after, discord.TextChannel):
            try:
                first_message_list = [message async for message in after.history(limit=123, oldest_first=True)]
                first_message: discord.Message = first_message_list[0]
                await after.edit(name=(first_message.mentions[0].display_name + "-" + first_message.channel.name.split("-")[-1])) # type: ignore
            except Exception as errorman:
                await after.guild.get_channel(1419741195424366612).send(str(errorman)) #type: ignore

if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
