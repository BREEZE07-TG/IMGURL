from IMGURL import app
from io import StringIO , BytesIO
import sys
import traceback
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message


owner = [5236678934]

async def aexec(code: str, app: Client, msg: Message):
    exec(
        "async def __aexec(app, msg): "
        + "\n p = print" 
        + "".join(f"\n {line}" for line in code.split("\n"))
    )
    return await locals()["__aexec"](app, msg)


@app.on_message(filters.command("exec"))
async def runPyro_Funcs(app: Client, msg: Message):
    if msg.from_user.id not in owner:
        await msg.reply("Sorry you are not authorised to use this command")
        return

    code_parts = msg.text.split(None, 1)
    if len(code_parts) == 1:
        return await msg.reply("Syntax Error: No code provided.")

    code = code_parts[1]
    message = await msg.reply(" Running...")

    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = StringIO(), StringIO()

    output, error, exception = None, None, None

    try:
        result = await aexec(code, app, msg)
    except Exception:
        exception = traceback.format_exc()

    output = sys.stdout.getvalue()
    error = sys.stderr.getvalue()

   
    sys.stdout, sys.stderr = old_stdout, old_stderr

    
    final_output = exception or error or output or result or "No output"

    response_text = (
        f"🖥️ **Code Executed:**\n"
        f"```python\n{code}\n```\n"
        f"📤 **Output:**\n"
        f"```Output\n{final_output}```"
    )

    
    if len(response_text) > 4000:
        response_text = response_text[:4000] + "\n\n Output truncated..."

    await message.edit(response_text)


@app.on_message(filters.command("bash"))
async def bash(client: Client, message: Message):
    if msg.from_user.id not in owner:
        await msg.reply("Sorry you are not authorised to use this command")
        return
    if len(message.command) < 2:
        return await message.reply("**Usage:** `/bash <command>`")

    cmd = message.text.split(" ", maxsplit=1)[1]
    
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    e = stderr.decode() or "No Error"
    o = stdout.decode() or "**Tip**: \n`If you want to see the results of your code, I suggest printing them to stdout.`"
    
    o = "`\n".join(o.split("\n"))
    
    OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"
    
    if len(OUTPUT) > 4095:
        with io.BytesIO(OUTPUT.encode()) as out_file:
            out_file.name = "exec.text"
            await message.reply_document(document=out_file, caption=cmd)
    else:
        await message.reply(OUTPUT)
