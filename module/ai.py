import torch
from transformers import pipeline as hf_pipeline
from IMGURL import app
from pyrogram import filters 

login(token="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")
def output(query):
    try:
        chat = [
            {"role": "system", "content": "You are a sassy, wise-cracking robot as imagined by Hollywood circa 1986."},
            {"role": "user", "content": query}
        ]
        generator = hf_pipeline(
            task="text-generation",
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        response = generator(chat, max_new_tokens=512)
        return response[0]["generated_text"][-1]["content"]
    except Exception as e:
        return str(e)

@app.on_message(filters.command("ai"))
async def ai(client, message):
    if len(message.command) < 2:
        return await message.reply("Please provide a prompt after the command.")
    text = message.text.split(maxsplit=1)[1]
    response = output(text)
    await message.reply(response)
 
