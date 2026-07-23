from dotenv import load_dotenv
import discord
import asyncio
import os
from mcname_api import get_uuid
import datetime

load_dotenv()
TOKEN = os.getenv("STATS_TOKEN")
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
    rest = splits[1:]
    action = None
    created_at = msg.created_at

    # join leave entry:
    if "joined" in rest:
        action = 1
    elif "left" in rest or "timed" in rest:
        action = 0
    
    if action in [0, 1]:
        return create_data_entry(username=name, action=action, date=created_at)
    
    # start/stop entry
    if "Started!" in rest:
        action = 2
    
    elif "Stopped!" in rest:
        action = 3
    
    if action in [2, 3]:
        return create_data_entry(username="Server", action=action, date=created_at)
    # print(name + "\t" + " ".join(rest))
    # print(splits)
    # print(created_at)


    


def convert_time(date_obj: datetime.datetime) -> str:
    """coverts a datetime object into a string of (date and time)

    Args:
        date_obj (datetime.datetime): the join/leave time of a player

    Returns:
        str: type casted tuple of data and time str ("d/m/Y", "H:M:S")
    """
    date = date_obj.strftime("%d/%m/%Y")
    time = date_obj.strftime("%H:%M:%S")
    return str((date + ";" +time))

def write_csv_entry(entry: str, filename):
    """Appends a given entry to the csv file 

    Args:
        entry (str): a string with the log in/out time and the fetched the uuid of a username 
    """
    print(f"Written entry: {entry}")
    with open(f"./ingame-activty/{filename}", "a") as f:
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
    if action in [0, 1, 2]:
        print(f"action = {action}")
    entry = ""
    if username != "Server":
        id: str | bool = get_uuid(username)
    else: 
        id = "0"
    
    if not id:  # means status code didnt return 200
        return False, "MC-username not found"
    date_entry: str = convert_time(date)
    if action == 1:  # action = join
        entry = ",".join([id, username, date_entry, "0"])  # type: ignore
        write_csv_entry(entry, "raw_activity.csv")
        return True, "Join entry written"

    elif action == 0:  # action = leave
        entry = ",".join([id, username, "0", date_entry])  # type: ignore
        write_csv_entry(entry, "raw_activity.csv")
        return True, "Leave entry written"

    elif action == 2:
        entry = ",".join(["Start", date_entry])  # type: ignore
        write_csv_entry(entry, "server_actions.csv")
        return True, "Start entry written"

    elif action == 3:
        entry = ",".join(["Stop", date_entry])  # type: ignore
        write_csv_entry(entry, "server_actions.csv")
        return True, "Stop entry written"

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
    
    channel = message.guild.get_channel(1011667712247857222) # type:ignore
    oldest_message = await channel.fetch_message(1516588773301817466) # type:ignore
    if message.content.startswith("/scrape") and message.author.id == 398769543482179585:
        async for message in channel.history(limit=None, oldest_first=True, after=oldest_message.created_at): #type:ignore
            if message.webhook_id and message.author.id == id_botclient and message.author.display_name == "Ethis Server":
                output = parse_message(message)
            
    # if (
    #     message.channel.id == id_mc_chat_channel
    #     and message.author.id == id_botclient
    #     and message.webhook_id
    #     and message.author.display_name == "Ethis Server"
    # ):  # basically only the achievements and leave and join
    #     output = parse_message(message)
    #     if not output[0] and message.guild:
    #         print(  # type:ignore
    #             output[1] + message.to_reference().jump_url
    #         ) 
    
    
    
    ### OLD:
        # if message.author.id != 398769543482179585:
    #     return
    
    # message_id = int(message.content)
    
    # message = await channel.fetch_message(message_id)
    #             # if not output[0] and message.guild:
    #             #     print(  # type:ignore
    #             #         output[1] + message.to_reference().jump_url
    #             #     ) 

if TOKEN:
    client.run(TOKEN)
else:
    raise ReferenceError("TOKEN doesnt exist")
