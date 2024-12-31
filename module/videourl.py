import os
import requests
import time
from pyrogram import Client, filters
from IMGURL import app

# Replace with your Vimeo Access Token
VIMEO_ACCESS_TOKEN = "153f42d592927f5e6026467978da72fb"

# Function to upload video to Vimeo
def upload_video_to_vimeo(video_path):
    """
    Uploads a video to Vimeo and returns the video link.
    
    Args:
        video_path (str): Path to the video file.
    
    Returns:
        str: Vimeo video link if successful, None otherwise.
    """
    url = "https://api.vimeo.com/me/videos"
    headers = {
        "Authorization": f"Bearer {VIMEO_ACCESS_TOKEN}"
    }
    files = {
        "file_data": open(video_path, "rb")
    }
    try:
        response = requests.post(url, headers=headers, files=files)
        response_data = response.json()
        if response.status_code == 200 and "link" in response_data:
            return response_data["link"]
        else:
            print(f"Error from Vimeo: {response_data}")
            return None
    except Exception as e:
        print(f"Error uploading video to Vimeo: {e}")
        return None
    finally:
        files["file_data"].close()

# Pyrogram video handler
@app.on_message(filters.incoming & filters.video)
async def handle_video_upload(client, message):
    start_time = time.time()
    reply = await message.reply("`Downloading video...`")
    
    # Download the video
    video_path = await client.download_media(message.video.file_id)
    if video_path:
        await reply.edit("`Uploading video to Vimeo...`")
        
        # Upload video to Vimeo
        video_url = await client.loop.run_in_executor(None, upload_video_to_vimeo, video_path)
        
        if video_url:
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            await reply.edit(f"`Video uploaded successfully!`\n\n"
                             f"**Vimeo URL:** {video_url}\n"
                             f"**Time Taken:** {elapsed_time:.2f} ms")
        else:
            await reply.edit("`Failed to upload the video to Vimeo.`")
        
        # Clean up the downloaded file
        if os.path.exists(video_path):
            os.remove(video_path)
    else:
        await reply.edit("`Failed to download the video.`")
                
