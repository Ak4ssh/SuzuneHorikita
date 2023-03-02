import asyncio

from pyrogram import idle
from src import suzune

print("Starting Suzune !")
    # STARTING BOT CLIENT
await suzune.start()




loop = asyncio.get_event_loop()
if __name__ == "__main__":
    loop.run_until_complete(startup())
