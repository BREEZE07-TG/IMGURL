from IMGURL import app
from pyrogram import Client, filters
import os
import aiohttp 
from pyrogram.enums import ParseMode
import time

IMGBB_API_KEY = "e3ab93774ab3b932602fc71aefec552f"

async def get_image_url(image_path):
   
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": IMGBB_API_KEY}
    
    try:
        
        async with aiohttp.ClientSession() as session:
            with open(image_path, "rb") as file:
                files = {"image": file}
                async with session.post(url, data=payload, data=files) as response:
                    response_data = await response.json()
                    if response_data["status"] == 200:
                     
                        return response_data["data"]["display_url"]
                    else:
                        print(f"Error from ImgBB: {response_data}")
                        return None
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

@app.on_message(filters.photo)
async def url_reply(client: Client, message):
    
    start_time = time.time()
    text = await message.reply("Uploading your image...")
    photo_path = await client.download_media(message.photo.file_id)

    if photo_path:
        
        image_url = await get_image_url(photo_path)

        if image_url:
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000  
            z = f'<a href="{image_url}">Link</a>'
            await text.edit(
                f"Your image is uploaded! Here's the URL: {z}\n\nTime taken: {elapsed_time:.3f} milliseconds\n`{image_url}`",
                parse_mode=ParseMode.HTML,
            )
        else:
            await text.edit("Failed to upload the image to ImgBB.")

        
        if os.path.exists(photo_path):
            os.remove(photo_path)
    else:
        await text.edit("Failed to download the photo.")
        
