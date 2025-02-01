from pyrogram import Client, filters
import os
import requests
import time
from pyrogram.enums import ParseMode
from IMGURL import app

parse_mode = ParseMode.HTML

CATBOX_API_URL = "https://catbox.moe/user/api.php"

def upload_to_catbox(image_path):
    """Uploads an image to Catbox.moe and returns the URL."""
    with open(image_path, "rb") as file:
        files = {"fileToUpload": (file.name, file)}
        data = {"reqtype": "fileupload", "userhash": ""}  # Empty userhash for anonymous uploads
        
        try:
            response = requests.post(CATBOX_API_URL, data=data, files=files)
            if response.status_code == 200:
                return response.text.strip()  # Catbox directly returns the image URL
            else:
                print(f"Error from Catbox: {response.text}")
                return None
        except Exception as e:
            print(f"Error uploading image: {e}")
            return None

@app.on_message(filters.photo & filters.private)
async def url_reply(client: Client, message):
    """Handles photo messages and uploads the image to Catbox."""
    start_time = time.time()
    text = await message.reply("Uploading your image...")
    photo_path = await client.download_media(message.photo.file_id)

    if photo_path:
        image_url = await client.loop.run_in_executor(None, upload_to_catbox, photo_path)

        if image_url:
            end_time = time.time()
            elapsed_time = end_time - start_time
            await text.edit(
                f"Your image has been uploaded!\n\n"
                f"<a href='{image_url}'>View Image</a>\n"
                f"Time taken: {elapsed_time:.3f} seconds\n"
                f"Direct Link: <code>{image_url}</code>",show_above_text = True
            )
        else:
            await text.edit("Failed to upload the image to Catbox.")

        if os.path.exists(photo_path):
            os.remove(photo_path)
    else:
        await text.edit("Failed to download the photo.")

@app.on_message(filters.command("url") & filters.reply)
async def url(client: Client, message):
    """Handles /url command and uploads the replied image to Catbox."""
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply("Please reply to an image.")
        return

    start_time = time.time()
    text = await message.reply("Uploading your image...")
    photo_path = await client.download_media(message.reply_to_message.photo.file_id)

    if photo_path:
        image_url = await client.loop.run_in_executor(None, upload_to_catbox, photo_path)

        if image_url:
            end_time = time.time()
            elapsed_time = end_time - start_time
            await text.edit(
                f"Your image has been uploaded! \n\n"
                f"<a href='{image_url}'>View Image</a>\n"
                f"Time taken: {elapsed_time:.3f} seconds\n"
                f"Direct Link: <code>{image_url}</code>",show_above_text = True
            )
        else:
            await text.edit("Failed to upload the image to Catbox.")

        if os.path.exists(photo_path):
            os.remove(photo_path)
    else:
        await text.edit("Failed to download the photo.")
