import requests
from pyrogram import Client, filters
from IMGURL import app
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os 
@app.on_message(filters.command("licence"))
async def licence(_, message):
    img_url = "https://i.ibb.co/PDTjQWG/photo-2025-01-01-03-45-46-7454788247634313240.jpg"
    response = requests.get(img_url)
    imag = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(imag)
    points = (68, 51)
    font1 = ImageFont.truetype("/usr/src/app/module/Fonts/Hey Comic.ttf", 40)
    string = "DEMON SLAYER GAME BOT"
    draw.text(points, string, "white", font=font1)
    imag.save("someone.jpg")

    await message.reply_photo("someone.jpg")

    
    os.remove("someone.jpg")
