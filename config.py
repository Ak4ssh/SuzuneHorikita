# (c) JigarVarma2005

import os

class Config(object):
	API_ID = int(os.environ.get("API_ID", "1234"))
	API_HASH = os.environ.get("API_HASH")
	BOT_TOKEN = os.environ.get("BOT_TOKEN")
	MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
