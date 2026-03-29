import os
from trello import TrelloClient
from dotenv import load_dotenv

load_dotenv()

trello_key = os.getenv("TRELLO_API_KEY")
trello_secret = os.getenv("TRELLO_API_SECRET")

client = TrelloClient(
    api_key="your-key",
    api_secret="your-secret",
)
all_boards = client.list_boards()
last_board = all_boards[-1]
print(last_board.name)
