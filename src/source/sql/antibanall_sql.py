import threading
from . import SESSION, BASE
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UnicodeText,
    UniqueConstraint,
    func,
)
from sqlalchemy.sql.sqltypes import BigInteger


class Antibanchats(BASE):
    __tablename__ = "Antiban-chats"
    chat_id = Column(BigInteger, primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def __repr__(self):
        return "<chats {}>".format(self.chat_id)

Antibanchats.__table__.create(checkfirst=True)
ILOCK = threading.RLock()

CHATS = []

def add(chat_id):
    fuk = SESSION.query(Antibanchats).get(chat_id)
    if not fuk:
       chat = Antibanchats(chat_id)
       CHATS.append(chat)
       SESSION.add(chat)
       SESSION.commit()

def remove(chat_id):
    with ILOCK:
        chat = SESSION.query(Antibanchats).get(chat_id)
        if chat:
            SESSION.delete(chat)
            SESSION.commit()
        else:
            SESSION.close()

def active(chat_id):
    try:
        return SESSION.query(Antibanchats).filter(Antibanchats.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()

def get_bans(chat_id: str, user_id) -> bool:
    if str(chat_id) in CHATS:
       count += 1
       if count > 5:
          """ Credits to RiZoeL & Akash """
          return True
       return False
