from sqlalchemy import Boolean, Column, String, UnicodeText
from src.source.sql import BASE, SESSION


class Antiban(BASE):
    __tablename__ = "Antiban"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Antiban.__table__.create(checkfirst=True)


def add_Antiban(chat_id: str):
    banmoddy = Antiban(str(chat_id))
    SESSION.add(banmoddy)
    SESSION.commit()


def rmAntiban(chat_id: str):
    rmbanmoddy = SESSION.query(Antiban).get(str(chat_id))
    if rmbanmoddy:
        SESSION.delete(rmbanmoddy)
        SESSION.commit()


def get_all_chat_id():
    stark = SESSION.query(Antiban).all()
    SESSION.close()
    return stark


def is_Antiban_indb(chat_id: str):
    try:
        s__ = SESSION.query(Antiban).get(str(chat_id))
        if s__:
            return str(s__.chat_id)
    finally:
        SESSION.close()
