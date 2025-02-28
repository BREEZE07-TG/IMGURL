from pyrogram import Client, filters
import ffmpeg
import os
from threading import Thread
from queue import Queue
from IMGURL import app

queue = Queue()
def progress(current, total, message, type):
    if type == "download":
        text = f"Downloading {current * 100 / total:.2f}%"
    elif type == "encode":
        text = f"Encoding {current * 100 / total:.2f}%"
    elif type == "upload":
        text = f"Uploading {current * 100 / total:.2f}%"
    app.edit_message_text(message.chat.id, message.id, text)

async def process_queue():
    while True:
        message = queue.get()
        try:
          
            if message.reply_to_message.video:
              
                video_file = await message.reply_to_message.download(progress=progress, progress_args=("download", message))
            elif message.reply_to_message.document and message.reply_to_message.document.mime_type.startswith("video/"):
               
                video_file = await message.reply_to_message.download(progress=progress, progress_args=("download", message))
            else:
                await message.reply("Please reply to a video message or file!")
                continue

           
            output_file = f"{os.path.splitext(video_file)[0]}_compressed.mp4"
            (
                ffmpeg
                .input(video_file)
                .map(0)
                .output(output_file,
                         vcodec="libx264",
                         pix_fmt="yuv420p",
                         crf=30,
                         preset="veryfast",
                         s="856x480",
                         acodec="aac",
                         ab=50*1024,
                         scodec="copy",
                         progress=progress,
                         progress_args=("encode", message))
                .run()
            )

            
            await message.reply_video(output_file, progress=progress, progress_args=("upload", message))

       
            os.remove(video_file)
            os.remove(output_file)
        except Exception as e:
            await message.reply(f"Error: {e}")
        finally:
            queue.task_done()

thread = Thread(target=process_queue)
thread.daemon = True
thread.start()

@app.on_message(filters.command("compress"))
async def compress_video(client, message):
    queue.put(message)
    await message.reply("Added to queue. Please wait...")

