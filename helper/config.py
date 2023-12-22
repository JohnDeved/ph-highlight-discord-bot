import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
if not DISCORD_TOKEN:
  raise ValueError("DISCORD_TOKEN is not set in the environment.")

GH_TOKEN = os.getenv("GH_TOKEN", "")
if not GH_TOKEN:
  raise ValueError("GH_TOKEN is not set in the environment.")