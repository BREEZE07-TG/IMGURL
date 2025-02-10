from IMGURL import app
from io import StringIO
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
        await message.reply("Sorry you are not authorised to use this command")
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
