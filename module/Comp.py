from pyrogram import Client, filters
import ffmpeg
import os
import asyncio
from IMGURL import app 

async def progress(current, total, message, type):
    try:
        text = f"{type.capitalize()} {current * 100 / total:.2f}%"
        await message.edit(text)
    except Exception as e:
        print(f"Progress update failed: {e}")

async def process_video(message):
    try:
        if message.reply_to_message.video:
            video_file = await message.reply_to_message.download(progress=progress, progress_args=(message, "Downloading"))
        elif message.reply_to_message.document and message.reply_to_message.document.mime_type.startswith("video/"):
            video_file = await message.reply_to_message.download(progress=progress, progress_args=(message, "Downloading"))
        else:
            await message.reply("Please reply to a valid video file!")
            return

        output_file = f"{os.path.splitext(video_file)[0]}_compressed.mp4"
        
        
        ffmpeg.input(video_file).output(output_file, vcodec="libx264", pix_fmt="yuv420p", crf=30, preset="veryfast", s="856x480", acodec="aac", ab="50k", scodec="copy").run()

        await message.reply_video(output_file, progress=progress, progress_args=(message, "Uploading"))

        os.remove(video_file)
        os.remove(output_file)
    except Exception as e:
        await message.reply(f"Error: {e}")

@app.on_message(filters.command("compress"))
async def compress_video(client, message):
    await message.reply("Processing video... Please wait.")
    await process_video(message)
        
