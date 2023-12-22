import requests
from helper.config import DISCORD_TOKEN

CHANNEL_ID = '1187741455876366387'

def send_file(path: str, content: str = ''):
    with open(path, 'rb') as f:
        return requests.post(
            f"https://discord.com/api/channels/{CHANNEL_ID}/messages",
            headers={"Authorization": f"Bot {DISCORD_TOKEN}"},
            files={"file": f},
            data={"content": content}
        )