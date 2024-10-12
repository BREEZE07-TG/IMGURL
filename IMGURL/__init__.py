from pyrogram import Client , filters
import logging
import config as c

FORMAT = "[IMGURL]: %(message)s"

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
                                                   logging.StreamHandler()], format=FORMAT)
plugins = {"root":"module"}

app = Client(
    "IMGURL", 
    api_id=c.api_id, 
    api_hash=c.api_hash,
    bot_token=c.bot_token,
    plugins=plugins
)
