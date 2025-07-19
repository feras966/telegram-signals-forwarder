from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import os

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
source_group_ids = os.environ.get("SOURCE_GROUP_IDS").split(",")
target_channel = os.environ.get("TARGET_CHANNEL")

keywords = ["buy", "sell"]

client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage(chats=[int(x) for x in source_group_ids]))
async def handler(event):
    if any(keyword in event.raw_text.lower() for keyword in keywords):
        if event.media:
            await client.send_file(target_channel, file=event.media, caption=event.raw_text)
        else:
            await client.send_message(target_channel, event.raw_text)

async def main():
    print("Bot is running...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())