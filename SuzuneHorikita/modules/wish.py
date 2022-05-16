#Copyright ©️ @TheVenomXD 

from random import randint 

from SuzuneHorikita.events import register
from SuzuneHorikita import telethn as tbot


@register(pattern=("/wish"))
async def awake(event):
    rem = randint(1, 100)
    await tbot.reply(f"Your wish has been cast.✨\n\nchance of success: {rem}% ")

