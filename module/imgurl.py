
from pyrogram import Client, filters
import os
import requests
import time
from pyrogram.enums import ParseMode
from IMGURL import app
parse_mode=ParseMode.HTML

IMGBB_API_KEY = "e3ab93774ab3b932602fc71aefec552f"

def get_image_url(image_path):
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBB_API_KEY,
    }
    with open(image_path, "rb") as file:
        files = {
            "image": file,
        }
        try:
            response = requests.post(url, data=payload, files=files)
            response_data = response.json()
            if response_data['status'] == 200:
                return response_data['data']['url']
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
        image_url = await client.loop.run_in_executor(None, get_image_url, photo_path)

        if image_url:
            imgurl = image_url
            end_time = time.time()
            elapsed_time = (end_time - start_time)
            z = f'<a href="{imgurl}">:</a>'
            await text.edit(f"Your image is uploaded! Here's the URL{z}\n\nTime taken: {elapsed_time:.3f} milliseconds\nLink: <code>{imgurl}</code> ", parse_mode)
        else:
            await text.edit("Failed to upload the image to ImgBB.")

        if os.path.exists(photo_path):
            os.remove(photo_path)
    else:
        await text.edit("Failed to download the photo.")
