from IMGURL import app
import openai
import time
from pyrogram import Client, filters

# Set your OpenAI API key
openai.api_key = "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"

# Define AI mode and logging channel
AI = True  # Enable AI responses
LOG_CHANNEL = -1001234567890  # Replace with your Telegram log channel ID

async def send_message_in_chunks(client, chat_id, text):
    """Send messages in chunks to avoid Telegram's character limit (4096)."""
    max_length = 4096
    for i in range(0, len(text), max_length):
        await client.send_message(chat_id, text[i:i + max_length])

@Client.on_message(filters.private & filters.text & ~filters.command(['start', 'broadcast']))
async def ai_answer(client, message):
    """Handles incoming private messages and responds with AI-generated answers."""
    if AI: 
        user_id = message.from_user.id
        if user_id:
            try:
                msg = await message.reply_text("**Please wait while I process your query...**")
                
                users_message = message.text
                
                # Generate AI response asynchronously
                response = await openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": users_message}
                    ],
                    max_tokens=1200,
                    temperature=0.6
                )
                
                ai_response = response["choices"][0]["message"]["content"].strip()
                
                footer_credit = (
                    "<b><a href='https://t.me/vj_bot_disscussion'>• Report Issue •</a>"
                    "══<a href='https://t.me/lightningboi'>• Contact Master •</a></b>"
                )
                
                # Delete the "please wait" message
                await msg.delete()
                
                # Send AI response to the user
                await send_message_in_chunks(client, message.chat.id, f"**Here is your answer:** 👇\n\n{ai_response}\n\n{footer_credit}")
                
                # Log user query and AI response
                log_message = (
                    f"**⭕ User:** {message.from_user.mention} (ID: {user_id})\n"
                    f"🔍 **Query:** `{users_message}`\n\n"
                    f"🖍 **Response:**\n{ai_response}\n\n"
                    f"🔻 **User ID:** {user_id} \n"
                    f"🔻 **Username:** {message.from_user.mention}"
                )
               
                
            except Exception as error:
                print(f"Error: {error}")
                await message.reply_text(f"**An error occurred:**\n\n{error}\n\n**Forward this to @lightningboi for support.**")
    else:
        return
              
