from IMGURL import app
from pyrogram import filters
import subprocess
import os
import asyncio
import sys
from module import exec as e

@app.on_message(filters.command('logs'))
async def logs(client,message):
  if message.from_user.id not in e.owner:
    await message.reply("You are not authorised to use this command")
    return 
  L = subprocess.getoutput("tail -n 20 logs.txt")
  await message.reply(f"<pre>Logs\n{L}</pre>")

@app.on_message(filters.command('restart'))
async def restart(client,message):
  if message.from_user.id not in e.owner:
    await message.reply("You are not authorised to use this command")
    return 
  rst_msg= await message.reply("restarting system...")
  await asyncio.sleep(2)
  subprocess.run(["python", "-m", "restart"])
  await rst_msg.edit("system restarted")
  os.execv(sys.executable, ['IMGURL'] + sys.argv)
