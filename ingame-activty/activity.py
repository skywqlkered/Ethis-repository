from dotenv import load_dotenv
import discord
import asyncio
import os
from mcname_api import get_uuid
import datetime

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)

id_mc_chat_channel = 1011667712247857222
id_botclient = 1437929768979796129
id_staff_bot = 1419741195424366612
id_sky = 398769543482179585


def parse_message(msg: discord.Message) -> tuple[bool, str]:
    """Parses a message and extracts action and mc username

    Args:
        msg (discord.Message): the message that will be parsed

    Returns:
        tuple[bool,str]: [0]: true if successfull; false otherwise
                         [1]: text output of operation
    """
    splits = msg.content.split(" ")
    name = splits[0]
    action = None
    if "joined" in splits[-1]:
        action = 1
    if splits[-1] == "left":
        action = 0

    # print(splits)
    created_at = msg.created_at
    # print(created_at)

    return create_data_entry(username=name, action=action, date=created_at)


def convert_time(date_obj: datetime.datetime) -> str:
    """coverts a datetime object into a string of (date and time)

    Args:
        date_obj (datetime.datetime): the join/leave time of a player

    Returns:
        str: type casted tuple of data and time str ("d/m/Y", "H:M:S")
    """
    date = date_obj.strftime("%d/%m/%Y")
    time = date_obj.strftime("%H:%M:%S")
    return str((date, time))


def write_csv_entry(entry: str):
    """Appends a given entry to the csv file 

    Args:
        entry (str): a string with the log in/out time and the fetched the uuid of a username 
    """
    with open("./ingame-activty/raw_activity.csv", "a") as f:
        f.write(entry + "\n")


def create_data_entry(
    username: str, action: int | None, date: datetime.datetime
) -> tuple[bool, str]:
    """Creates a string with the log in/out time and the fetched the uuid of a username

    Args:
        username (str): the mc username
        action (int | None): either 1 for join, 0 for leave or None if action isnt clear
        date (datetime.datetime): the join/leave time

    Returns:
        tuple[bool, str]: [0]: true if successfull; false otherwise
                          [1]: text output of operation
    """
    print(f"action = {action}")
    entry = ""
    id: str | bool = get_uuid(username)
    if not id:  # means status code didnt return 200
        return False, "MC-username not found"
    date_entry: str = convert_time(date)
    if action == 1:  # action = join
        entry = ",".join([id, username, date_entry, "0"])  # type: ignore
        write_csv_entry(entry)
        return True, "Join entry written"

    elif action == 0:  # action = leave
        entry = ",".join([id, username, "0", date_entry])  # type: ignore
        write_csv_entry(entry)
        return True, "Leave entry written"

    else:
        return False, "action wasnt clear"


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    # if message.author.id == 398769543482179585:
    #     channel_msg = client.get_channel(id_mc_chat_channel)
    #     if isinstance(channel_msg, discord.TextChannel):  # test message part
    #         msg_id = message.content
    #         try:
    #             msg_id_int = int(msg_id)
    #         except:
    #             return
    #         mesg = await channel_msg.fetch_message(msg_id_int)
    #         parse_message(mesg)

    if (
        message.channel.id == id_staff_bot
        and message.author.id == id_sky
        and not message.webhook_id
    ):  # basically only the achievements and leave and join
        output = parse_message(message)
        if not output[0] and message.guild:
            await message.guild.get_channel(id_staff_bot).send(  # type:ignore
                output[1] + message.to_reference().jump_url
            ) 

if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
