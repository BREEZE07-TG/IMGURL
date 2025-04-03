from IMGURL import app
from pyrogram import Client, filters  
from pyrogram.types import InlineKeyboardButton , InlineKeyboardMarkup

@app.on_message(filters.command('start'))        
async def start_handler(client, message):
    await client.send_photo(
        chat_id=message.chat.id,
        photo="https://i.ibb.co/nMSHkfJ/photo-2024-10-03-17-58-50.jpg",
        caption="**--This is an advanced image to URL generator bot--**\n\n"
                "> What can this bot do:\n"
                "<pre>Supports multi media Url\n"
                "Usage: \n"
                "In group use /url & in pvt directly send that media\n</pre>"\n\n
                f"{"➖"*15}\n"
                "Click on \"manual\" for more details"\n
                "➖"*15,
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("manual",url="https://test-oirz.onrender.com")]])
                
        reply_to_message_id=message.id
    )
    
  
