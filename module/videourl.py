import os
import time
import requests
from pyrogram import Client, filters
from IMGURL import app

# Correct Catbox API URL
CATBOX_API_URL = "https://catbox.moe/upload.php"

# Function to upload GIF to Catbox
def upload_gif_to_catbox(gif_path):
    """
    Uploads the GIF to Catbox and returns the file URL.
    """
    with open(gif_path, "rb") as file:
        try:
            files = {"fileToUpload": file}
            response = requests.post(CATBOX_API_URL, files=files)
            response_data = response.json()
            
            if response_data["success"]:
                return response_data["url"]
            else:
                print(f"Error from Catbox: {response_data}")
                return None
        except Exception as e:
            print(f"Error uploading GIF to Catbox: {e}")
            return None

# Pyrogram bot
@app.on_message(filters.video & filters.animation )
async def handle_gif_upload(client, message):
    start_time = time.time()
    reply = await message.reply("`Downloading GIF...`")
    
    # Download the GIF
    gif_path = await client.download_media(message.animation.file_id)
    if gif_path:
        await reply.edit("`Uploading GIF to Catbox...`")
        
        # Upload GIF to Catbox
        gif_url = await client.loop.run_in_executor(None, upload_gif_to_catbox, gif_path)
        
        if gif_url:
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            await reply.edit(f"`GIF uploaded successfully!`\n\n"
                             f"**Catbox URL:** {gif_url}\n"
                             f"**Time Taken:** {elapsed_time:.2f} ms")
        else:
            await reply.edit("`Failed to upload the GIF to Catbox.`")
        
        # Clean up the downloaded file
        if os.path.exists(gif_path):
            os.remove(gif_path)
    else:
        await reply.edit("`Failed to download the GIF.`")
        
