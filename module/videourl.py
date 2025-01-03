import os
import time
import requests
from pyrogram import Client, filters
from IMGURL import app

#Here's an example of how you can create a `/licence` command using Pyrogram that generates an image with the specified text:
#from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont
#import requests
from io import BytesIO

#Here's the modified code that uses the `os` module to remove the temporary image file after sending it:


#from pyrogram import Client, filters
#from PIL import Image, ImageDraw, ImageFont
#import requests
#from io import BytesIO
#import os

#app = Client("my_account")

@app.on_message(filters.command("licence"))
async def licence(_, message):
    img_url = "https://i.ibb.co/PDTjQWG/photo-2025-01-01-03-45-46-7454788247634313240.jpg"
    response = requests.get(img_url)
    imag = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(imag)
    points = (68, 51)
    font1 = ImageFont.truetype("/IMGURL/module/Fonts/Hey Comic.ttf", 40)
    string = "DEMON SLAYER GAME BOT"
    draw.text(points, string, "white", font=font1)
    imag.save("someone.jpg")

    await message.reply_photo("someone.jpg")

    # Remove the temporary image file
    os.remove("someone.jpg")

#app.run()


#This code uses the `os.remove()` function to delete the "someone.jpg" file after it's been sent as a photo. This helps keep your temporary files organized and avoids cluttering your file system.
