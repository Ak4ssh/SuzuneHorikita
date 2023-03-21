import sys
from pyrogram import idle
from . import suzune

if __name__ == "__main__":
    try:
       suzune.start()
       print("Bot Started!")
    except Exception as eror:
       print(str(error))
       sys.exit()
    idle()
