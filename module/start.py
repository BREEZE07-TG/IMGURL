from IMGURL import app
from pyrogram import Client, filters 

@app.on_message(filters.command('start'))        
async def start_handler(client,message):
               await client.send_photo(message.chat.id,"https://i.ibb.co/nMSHkfJ/photo-2024-10-03-17-58-50-7421610415546695696.jpg",
               "**--This is an advanced image to url genrater bot--**\n\n"
               ">What can this bot do:\n"
               "<pre>Currently this bot can provide any photo url under 50mb\nI hope many features would be added soon! \nplease send me any photo to continue</pre>")       

