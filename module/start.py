from IMGURL import app
from pyrogram import Client, filters  
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command('start'))        
async def start_handler(client, message):
    await client.send_photo(
        message.chat.id,
        "https://i.ibb.co/nMSHkfJ/photo-2024-10-03-17-58-50.jpg",
        "**--This is an advanced image to URL generator bot--**\n\n"
        "> **What can this bot do:**\n"
        "<pre>Supports multi-media URLs\n"
        "Usage: \n"
        "In group: use /url\n"
        "In private: send media directly</pre>\n\n"
        "➖" * 15 + "\n"
        "Click on \"Manual\" for more details\n"
        "➖" * 15,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Manual", url="https://test-oirz.onrender.com")]
        ]),
        reply_to_message_id=message.id
    )
