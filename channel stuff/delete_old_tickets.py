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
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.id == 398769543482179585 and message.content.startswith('/del channels'):

        applog1 = message.guild.get_channel(1501309587951718430)
        # applog3 = message.guild.get_channel(1454240733056729128)
        # applog4 = message.guild.get_channel(1226215932704325702)

        # applog5: discord.CategoryChannel = message.guild.get_channel(1294969300725141655)
        # staffapp: discord.CategoryChannel = message.guild.get_channel(1420506502506090516)

        # whitelist: discord.CategoryChannel = message.guild.get_channel(1420508979318096006)
        whitelistp2: discord.CategoryChannel = message.guild.get_channel(
            1420534780658974720)
        # whitelistp3: discord.CategoryChannel = message.guild.get_channel(1420537439012913323)
        # ticket: discord.CategoryChannel = message.guild.get_channel(1420509042367004752)

        # whitelists2: discord.CategoryChannel = message.guild.get_channel(1420525392145416302)
        # tickets2: discord.CategoryChannel = message.guild.get_channel(1420530121936343160)

        # stringe = "closed-0042"
        # number = stringe.split("-")[1]

        for channel in applog1.text_channels:
            channel: discord.TextChannel
            
            first_message_list: list[discord.Message] = [message async for message in channel.history(limit=1,oldest_first=True)]
            first_message: discord.Message = first_message_list[0]
            if not message.guild.get_member(first_message.mentions[0].id):
                await channel.delete(reason="Member left.")

                print("deleted ", channel.name)

            await asyncio.sleep(0.5)

        print("done deleting")

if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
