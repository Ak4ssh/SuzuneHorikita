#Copyright ©️ @TheVenomXD 

from random import randint 

from SuzuneHorikita.events import register
from SuzuneHorikita import telethn as tbot


@register(pattern=("/wish"))
async def awake(event):
    rem = randint(1, 100)
        TEXT = f"Your wish has been cast.✨\n\nchance of success: {rem}%  "
        await tbot.send_file(event.chat_id, caption=TEXT)

