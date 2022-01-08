from typing import Text
from dotenv import dotenv_values
import slack

config = dotenv_values(dotenv_path=".env")

client = slack.WebClient(token=config["SLACK_TOKEN"])

client.chat_postMessage(channel="#random", text="Welcome to notifIEEE")
