import asyncio

from pyrogram import idle

from . import suzune
               
async def startup():
    # STARTING CLIENTS
    await suzune.start()


loop = asyncio.get_event_loop()
if __name__ == "__main__":
    loop.run_until_complete(startup())
