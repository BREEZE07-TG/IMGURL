from IMGURL import app
from pyrogram import Client, filters
import os
import requests
import time

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
  text = await message.reply("Uploading your image...") # Initial message
  photo_path = await client.download_media(message.photo.file_id)

  if photo_path:
    image_url = await client.loop.run_in_executor(None, get_image_url, photo_path)
    
    if image_url:
      end_time = time.time() # Calculate end time after upload
      elapsed_time = (end_time - start_time) * 1000 # Convert to milliseconds
      await text.edit("Your image is uploaded! Here's the URL:\n\n"
                f"Time taken: {elapsed_time:.2f} milliseconds\n"
                f"{image_url}")
    else:
      await text.edit("Failed to upload the image to ImgBB.")
    
    if os.path.exists(photo_path):
      os.remove(photo_path)
  else:
    await text.edit("Failed to download the photo.")
      
