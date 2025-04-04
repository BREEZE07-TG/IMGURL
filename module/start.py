from DS import app
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from config import sudo
import random
import re

database = {}

@app.on_message(filters.command("start"))
async def start(client,message):
    user = message.from_user
    if user.id not in sudo:
        return
    chat_type = message.chat.type
    if chat_type != ChatType.PRIVATE:
        await message.reply("This command only works in Private")
        return
    database[user.id] = {"gender":"undifined","status":"alive","name":"none"}
    await client.send_video(
        message.chat.id,
        "https://files.catbox.moe/9f9bvs.mp4",
        f"〖𝐃𝐄𝐌𝐎𝐍 𝐒𝐋𝐀𝐘𝐄𝐑: 𝐑𝐈𝐒𝐄 𝐎𝐑 𝐅𝐀𝐋𝐋〗\n\n"
        "❛A world shrouded in darkness…  \n"
        "⚔️ The final battle is near… ❜\n\n"
        f"🔥 𝐓𝐖𝐎 𝐏𝐀𝐓𝐇𝐒. 𝐎𝐍𝐄 𝐃𝐄𝐒𝐓𝐈𝐍𝐘. 🔥  \n\n"
        "❂ 𝐒𝐋𝐀𝐘𝐄𝐑𝐒 – Wield your blade, master Breathing, and protect humanity.  \n"
        "✶ 𝐃𝐄𝐌𝐎𝐍𝐒 – Consume power, evolve beyond limits, and rule the night.  \n\n"
        "𝐄𝐕𝐄𝐑𝐘 𝐂𝐇𝐎𝐈𝐂𝐄 𝐂𝐇𝐀𝐍𝐆𝐄𝐒 𝐘𝐎𝐔𝐑 𝐏𝐀𝐓𝐇...  \n"
        "What will you become?  \n\n"
        "[𝐁𝐄𝐆𝐈𝐍 𝐘𝐎𝐔𝐑 𝐉𝐎𝐔𝐑𝐍𝐄𝐘 𝐍𝐎𝐖!]",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"S T A R T", callback_data="start_data")]]),
        reply_to_message_id=message.id
        )


@app.on_callback_query(filters.regex(r"start_data$"))
async def enter(Client, CallbackQuery):
    user_id = CallbackQuery.from_user.id
    if user_id not in database:
        database[user_id] = {"gender": "undefined", "status": "alive", "name": "none"}

    await CallbackQuery.message.delete()
    await Client.send_photo(CallbackQuery.message.chat.id,"https://files.catbox.moe/x3m40x.jpg", "<b>Welcome player!</b>\nLets Begain With Your Name-\nPlease Enter Your Name: ")

@app.on_message(filters.text & filters.private)
async def get_name(client, message):
    user_id = message.from_user.id
    if user_id in database and database[user_id]["name"] == "none":
        database[user_id]["name"] = message.text

        confirmation = await message.reply(f"Your name has been set to {database[user_id]['name']}")
        await asyncio.sleep(1)
        await confirmation.delete()

        await client.send_message(
            message.chat.id,
            "Please select your gender[.](https://files.catbox.moe/g1j35m.jpg)",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"BOY", callback_data="boy"),
                 InlineKeyboardButton(f"GIRL", callback_data="girl")]
            ])
        )
                
@app.on_callback_query(filters.regex(r"^(boy|girl)$"))
async def gender_selection(Client,CallbackQuery):
        data = CallbackQuery.data
        user_id = CallbackQuery.from_user.id
        data_state = database[user_id]
        if data == "boy":
            data_state['gender'] = "boy"
            await asyncio.sleep(1)
            await CallbackQuery.edit_message_text(
                "You have selected your journey as a boy[.](https://files.catbox.moe/3e3mkc.jpg)\n",
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"View Stats" , callback_data= "stats"),
                                                      InlineKeyboardButton(f"BACK" , callback_data= "gen")]])
            )
        if data == "girl":
            data_state['gender'] = "girl"
            await asyncio.sleep(1)
            await CallbackQuery.edit_message_text(
                "You have selected your journey as a girl[.](https://files.catbox.moe/nlc352.jpg)\n",
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"View Stats" , callback_data= "stats"),
                                                      InlineKeyboardButton(f"BACK" , callback_data= "gen")]])
            )

@app.on_callback_query(filters.regex(r"gen$"))
async def ling(client,CallbackQuery):
    data = CallbackQuery.data
    if data == "gen":
            await CallbackQuery.edit_message_text(
            "Please select your gender[.](https://files.catbox.moe/g1j35m.jpg)",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"BOY", callback_data="boy"),
                 InlineKeyboardButton(f"GIRL", callback_data="girl")]
            ])
        )
        
@app.on_callback_query(filters.regex(r"stats$"))
async def vs(Client,CallbackQuery):
    data = CallbackQuery.data
    user_id = CallbackQuery.from_user.id
    data_state = database[user_id]
    markup = [[InlineKeyboardButton("BACK" , callback_data= "bck")],[InlineKeyboardButton("CONTINUE", callback_data="aage")]]
    female_text = "⚔️ Character Stats ⚔️\n✦ Core Stats\n───────────────────────\n◆ [STR] Strength: 8\n◆ [AGI] Agility: 12\n◆ [END] Endurance: 9\n◆ [BB] Breathing Bar: 10\n◆ [INT] Intelligence: 10\n◆ [PER] Perception: 11\n\n✦ Secondary Stats\n───────────────────────\n◆ [HP] Health Points: 90\n◆ [STA] Stamina: 95\n◆ [SP] Skill Power: 100\n◆ [DEF] Defense: 18\n◆ [CRIT] Critical Rate: 11%"
    male_text = "⚔️ Character Stats ⚔️\n✦ Core Stats\n\n───────────────────────\n◆ [STR] Strength: 10\n◆ [AGI] Agility: 8\n◆ [END] Endurance: 12\n◆ [BB] Breathing Bar: 10\n◆ [INT] Intelligence: 9  \n◆ [PER] Perception: 9\n\n✦ Secondary Stats\n───────────────────────\n◆ [HP] Health Points: 120  \n◆ [STA] Stamina: 110  \n◆ [SP] Skill Power: 100  \n◆ [DEF] Defense: 24  \n◆ [CRIT] Critical Rate: 9%\n"
    if data == "stats":
        if data_state['gender'] == "boy":
            await CallbackQuery.edit_message_text(male_text,reply_markup = InlineKeyboardMarkup(markup))
        else:
            await CallbackQuery.edit_message_text(female_text,reply_markup = InlineKeyboardMarkup(markup))

@app.on_callback_query(filters.regex(r"bck$"))
async def aagee(Client,CallbackQuery):
    data = CallbackQuery.data
    user_id = CallbackQuery.from_user.id
    data_state = database[user_id]
    if data == "bck":
        if data_state["gender"] == "boy":
            await CallbackQuery.edit_message_text(
                "You have selected your journey as a boy[.](https://files.catbox.moe/3e3mkc.jpg)\n",
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"View Stats" , callback_data= "stats"),
                                                      InlineKeyboardButton(f"BACK" , callback_data= "gen")]])
            )
        else:
            await CallbackQuery.edit_message_text(
                "You have selected your journey as a girl[.](https://files.catbox.moe/nlc352.jpg)\n",
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"View Stats" , callback_data= "stats"),
                                                      InlineKeyboardButton(f"BACK" , callback_data= "gen")]])
            )


@app.on_callback_query(filters.regex(r"aage$"))
async def aagee(Client,CallbackQuery):
    data = CallbackQuery.data
    if data == "aage":
        await CallbackQuery.message.delete()
        await Client.send_photo(
                        CallbackQuery.message.chat.id,
                        "https://files.catbox.moe/qk1vr2.jpg",
                        "<blockquote>Chapter 1: DESTINY BEGINS WITH DEATH</blockquote>",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"BEGIN", callback_data="begin")]]))

@app.on_callback_query(filters.regex(r"begin$"))
async def begain(Client,CallbackQuery):
    data = CallbackQuery.data
    if data == "begin": 
        await CallbackQuery.message.delete()
        await asyncio.sleep(1)
        await Client.send_photo(
                CallbackQuery.message.chat.id,
                "https://files.catbox.moe/kygjzd.jpg",
                "<blockquote>Narration</blockquote>"
                "<b>The rich aroma of coffee fill the air. Sunlight streams through the windows, casting a warm glow. Outside, the city hums with life, but in here-it's peceful.</b>\n\n"
                "<b>The protagonist leans back, sipping their drink. Across from them, Renji stirs his coffee, a faint smile playing on his lips. For now, outside doens't matter</b>",
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"NEXT" , callback_data= "next")]]))
   


@app.on_callback_query(filters.regex(r"next$"))
async def begain(Client,CallbackQuery):
    data = CallbackQuery.data
    user_id = CallbackQuery.from_user.id
    data_state = database[user_id]
    if data == "next": 
        await CallbackQuery.message.delete()
        await asyncio.sleep(1)
        await Client.send_photo(
            CallbackQuery.message.chat.id,
            "https://files.catbox.moe/g6zxhf.jpg",
            "<blockquote>Renji</blockquote>\n\n"
            "<b>\"You always get that look when we're here. What is it about this place that gets you so sentimental\"</b>\n\n"
            "<blockquote>CHOOSE YOUR RESPONCE</blockquote>\n"
            "<pre>Choice 1: \"It's the little things that make life enjoyable.\"\n"
            "Choice 2: \"Maybe I just like good coffee and good company.\"\n"
            "Choice 3: \"I dunno, maybe I'm just weird like that.\"</pre>",
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"Choice 1" , callback_data= "c1r1"),
                                                  InlineKeyboardButton(f"Choice 2" , callback_data= "c1r2")],
                                                 [InlineKeyboardButton(f"Choice 3" , callback_data= "c1r3")]])
        )
 


@app.on_callback_query(filters.regex(r"^(c1r1|c1r2|c1r3)$"))  #eg - c1r1 = chapter 1 responce 1
async def ch1res(Client,CallbackQuery):
    data = CallbackQuery.data
    ch1responces = [[InlineKeyboardButton(f"CONTINUE" , callback_data= "continue")]]
    if data == "c1r1":
        await CallbackQuery.message.delete()
        await asyncio.sleep(1)
        await Client.send_photo(
            CallbackQuery.message.chat.id,
            "https://files.catbox.moe/8tpqtd.jpg",
            "<blockquote>Renji</blockquote>\n"
            "\"<b>You know, that’s kinda nice. We always focus on big dreams and what’s next, but maybe moments like this matter just as much.</b>\"\n\n"
            "<blockquote>Name</blockquote>\n"
            "\"<b>See? You’re getting sentimental too.</b>\"\n\n"
            "<blockquote>Renji</blockquote>\n"
            "\"<b>Yeah, yeah, don’t get used to it.</b>\"",
            reply_markup = InlineKeyboardMarkup(ch1responces),
        )
    if data == "c1r2":
        await CallbackQuery.message.delete()
        await asyncio.sleep(1)
        await Client.send_photo(
            CallbackQuery.message.chat.id,
            "https://files.catbox.moe/fdkkz2.jpg",
            "<blockquote>Renji</blockquote>\n"
            "\"<b>Well, at least one of those is true. I’ll let you decide which one.</b>\"\n\n"
            "<blockquote>Name</blockquote>\n"
            "\"<b>Hmm… tough choice.</b>\"\n\n"
            "<blockquote>Renji</blockquote>\n"
            "\"<b>If you say anything other than me, I’m walking out.</b>\"\n\n"
            "<blockquote>Name</blockquote>\n"
            "\"<b>Alright, alright. You win this time.</b>\"",
            reply_markup = InlineKeyboardMarkup(ch1responces),
        )
    if data == "c1r3":
        await CallbackQuery.message.delete()
        await asyncio.sleep(1)
        await Client.send_photo(
            CallbackQuery.message.chat.id,
            "https://files.catbox.moe/wx9zo3.jpg",
            "<blockquote>Renji</blockquote>\n"
            "\"<b>Weird is one way to put it. I was thinking more along the lines of ‘hopeless romantic stuck in a coffee commercial.’</b>\"\n\n"
            "<blockquote>Name</blockquote>\n"
            "\"<b>Hey, if my life was a commercial, at least I’d get free coffee.</b>\"\n\n",
            reply_markup = InlineKeyboardMarkup(ch1responces),
        )
@app.on_callback_query(filters.regex(r"continue"))
async def cont(Client,CallbackQuery):
    data = CallbackQuery.data
    if data == "continue":
        await CallbackQuery.message.delete()
        await asyncio.sleep(1)
        await Client.send_photo(
            CallbackQuery.message.chat.id, 
            "https://files.catbox.moe/rhqyuf.jpg",
            ">Emi\n"
            "\"<b>You two again? At this point café should just give you a VIP pass.</b>\"\n\n"
            ">CHOOSE YOUR RESPONCE\n"
            "<pre>Choice 1: \"Well, you did say this place had the best cinnamon rolls.\"\n"
            "Choice 2: \"We’re basically part of the furniture here now.\"\n"
            "Choice 3: \"Blame Renji. He’s addicted to their coffee.\"</pre>",
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"Choice 1" , callback_data= "c1r1c2"),
                                                  InlineKeyboardButton(f"Choice 2" , callback_data= "c1r2c2")],
                                                 [InlineKeyboardButton(f"Choice 3" , callback_data= "c1r3c2")]])
        )   

@app.on_callback_query(filters.regex(r"^(c1r1c2|c1r2c2|c1r3c2)$"))  #eg - c1r1c2 = chapter 1 responce 1 choice 2
async def ch1resc2(Client,CallbackQuery):
        data = CallbackQuery.data
        cnt =  [[InlineKeyboardButton(f"CONTINUE" , callback_data= "cont")]]
        if data == "c1r1c2":
            await CallbackQuery.message.delete()
            await asyncio.sleep(1)
            res = await Client.send_photo(
                CallbackQuery.message.chat.id,
                "https://files.catbox.moe/1dqos1.jpg",
                ">Emi\n"
                "\"<b>And I was right, wasn’t I?</b>\"\n\n"
                ">Name\n"
                "\"<b>You were. This might actually be the best thing I’ve ever tasted.</b>\"\n\n"
                ">Emi\n"
                "\"<b>Told you. I should start charging for my food recommendations.</b>\"\n\n"
                ">Renji\n"
                "\"Nah, you'd just make us all broke.</b>\"\n\n",
                reply_markup = InlineKeyboardMarkup(cnt)

 
            )
        if data == "c1r2c2":
            await CallbackQuery.message.delete()
            await asyncio.sleep(1)
            res = await Client.send_photo(
                CallbackQuery.message.chat.id,
                "https://files.catbox.moe/16hf53.jpg",
                ">Emi\n"
                "\"<b>Great, now I have to start dusting you guys off before my shift starts.</b>\"\n\n"
                ">Name\n"
                "\"<b>Hey, we’re classy furniture. Maybe a fancy leather couch or something.</b>\"\n\n"
                ">Emi\n"
                "\"<b>Nah, more like an old, worn-out beanbag chair.</b>\"\n\n"
                ">Renji\n"
                "\"<b>Wow. That’s the rudest thing anyone has ever said to me.</b>\"\n\n"
                ">Emi\n"
                "\"<b>And yet, you’ll still be here tomorrow.</b>\"",
                reply_markup = InlineKeyboardMarkup(cnt)
            )
        if data == "c1r3c2":
            await CallbackQuery.message.delete()
            await asyncio.sleep(1)
            res = await Client.send_photo(
                CallbackQuery.message.chat.id,
                "https://files.catbox.moe/joz0w9.jpg",
                ">Renji\n"
                "\"<b>It’s true. This coffee owns my soul now.</b>\"\n\n"
                ">Emi\n"
                "\"<b>I knew you were too weak to resist.</b>\"\n\n"
                ">Renji\n"
                "\"<b>Hey, I have no regrets. If this is how I go out, at least I’ll be caffeinated.</b>\"\n\n"
                ">Name\n"
                "\"<b>Rest in peace, buddy. We’ll put a cup of coffee on your grave.</b>\"\n\n"
                ">Emi\n"
                "\"<b>Make it a double shot. He’d want it that way.</b>\"\n\n",
                reply_markup = InlineKeyboardMarkup(cnt)
            )

@app.on_callback_query(filters.regex(r"cont$"))
async def enter(Client, CallbackQuery):
    user_id = CallbackQuery.from_user.id 
    await CallbackQuery.message.delete()
    await Client.send_photo(
            CallbackQuery.message.chat.id,
            "https://files.catbox.moe/gmw7vz.jpg",
            ">Narration\n\n"
            "<b>The sky glows with shades of orange and pink. The protagonist leans back, a rare sense of peace settling in.</b>\n\n"
            ">Name\n"
            "\"<b>You know… I don’t need anything more than this. Just good coffee, good food, and good friends.</b>\"\n\n"
            ">Renji\n"
            "\"Careful, you're tempting fate. Say something like that, and the universe might just decide to mess with you.</b>\"\n\n"
            "<b>End Of Scene 1</b>",
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Move To Scene 2 ⇨", callback_data="s2")]]))      

        
#END OF SCENE 1
#SCENE 2



@app.on_callback_query(filters.regex(r"s2$"))
async def s20(Client,CallbackQuery):
    data = CallbackQuery.data
    if data == "s2":
        await CallbackQuery.message.delete()
        await Client.send_photo(
            CallbackQuery.message.chat.id,
            "https://files.catbox.moe/tdo7ur.jpg",
            "<b>The once-bustling streets have quieted, the soft hum of distant chatter mixing with the occasional rustle of leaves. Streetlights flicker, casting long, shifting shadows.\n\nA faint breeze drifts through the alleyways, carrying a whisper of something unseen. Footsteps echo—but not theirs.</b>",
            reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("NEXT ⇾",callback_data="s2story")]]
            ))
        

@app.on_callback_query(filters.regex(r"s2story$"))
async def nexts2y(Client,CallbackQuery):
    data = CallbackQuery.data
    user_id = CallbackQuery.from_user.id
    data_state = database[user_id]
    if data_state["gender"] == "boy":
        pic = "https://files.catbox.moe/sbq892.jpg"
    else:
        pic = "https://files.catbox.moe/lt1qve.jpg"
    if data == "s2story":
        await CallbackQuery.message.delete()
        await Client.send_photo(
            CallbackQuery.message.chat.id,
            pic,
            ">Renji\n"
            "\"<b>Man, that was a good way to end the day. Too bad we have class tomorrow.</b>\"\n\n"
            ">Protagonist\n"
            "\"<b>Assuming you even show up.</b>\"\n\n"
            ">Renji\n"
            f"\"<b>Hey, I have a 75% attendance rate. That’s basically an A for effort.</b>\"",
            reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("NEXT ⇾",callback_data="nexts2o")]]
            ))
@app.on_callback_query(filters.regex(r"nexts2o$"))
async def nexts2oy(Client,CallbackQuery):
    data = CallbackQuery.data
    if data == "nexts2o":
        await CallbackQuery.message.delete()
        await Client.send_photo(
            CallbackQuery.message.chat.id,
            "https://files.catbox.moe/9qnv4d.jpg",
            ">????\n"
            "<b>\"Got a minute?\"</b>\n\n"
            ">CHOOSE YOUR RESPONSE\n"
            "<pre>Choice 1: \"Uh, sorry, we’re in a hurry.\"\n" 
            "Choice 2: \"Who the hell are you?\"\n"
            "Choice 3: \"Depends. What do you want?\"</pre>",
            reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Choice 1",callback_data="c1s2r1"),
                      InlineKeyboardButton("Choice 2",callback_data="c1s2r2")],
                    [InlineKeyboardButton("Choice 3",callback_data="c1s2r3")]]
                ))          


@app.on_callback_query(filters.regex(r"^(c1s2r1|c1s2r2|c1s2r3)$")) #c1s2r1 = cahpter 1 scene 2 responce 1
async def s2c1(Client,CallbackQuery):
    data = CallbackQuery.data
    if data == "c1s2r1":
        await CallbackQuery.message.delete()
        await Client.send_photo(
            CallbackQuery.message.chat.id,
            "https://files.catbox.moe/ixn92a.jpg",
            ">Hooded Man\n"
            "<b>\"Yeah? Well, so am I. Hand over your wallets, and we’ll all be on our way.\"</b>\n\n"
            ">Renji\n"
            "<b>\"Crap… mugger. What do we do?\"</b>\n\n"
            ">CHOOSE YOUR RESPONSE\n"
            "<pre>Choice 1: Give him the money and leave.\n"
            "Choice 2: Try to run.\n"
            "Choice 3: Stand your ground.</pre>",
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Choice 1",callback_data="c1s2o_GiveMoney"),
                  InlineKeyboardButton("Choice 2",callback_data="c1s2o2_Run")],
                 [InlineKeyboardButton("Choice 3",callback_data="c1s2o2_Stand")]]
            )
        )
    if data == "c1s2r2":
        await CallbackQuery.message.delete()
        await Client.send_photo(
            CallbackQuery.message.chat.id,
            "https://files.catbox.moe/t8v754.jpg",
            ">Hooded Man\n"
            "<b>\"Wrong answer.\"</b>\n\n"
            "<i>Without warning, he pulls out a knife, the blade glinting under the streetlight.</i>\n\n"
            ">Renji\n"
            "<b>\"Shit—he’s serious!\"</b>\n\n"
            ">CHOOSE YOUR RESPONSE\n"
            "<pre>Choice 1: Try To Fight Him Off\n"
            "Choice 2: Tell Renji To Run While You Distract Him\n"
            "Choice 3: Try To De-Escalate The Situation</pre>",
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Choice 1",callback_data="c1s2o2_Fight"),
                 InlineKeyboardButton("Choice 2",callback_data="c1s2o2_Distract")],
                 [InlineKeyboardButton("Choice 3",callback_data="c1s2o2_Esclate")]]
            )
        )
    if data == "c1s2r3":
        await CallbackQuery.message.delete()
        await Client.send_photo(
            CallbackQuery.message.chat.id,
            "https://files.catbox.moe/vjgcjw.jpg",
            ">Hooded Man\n"
            "<b>\"Smart kid. Maybe you can make this easy.\"</b>\n\n"
            "<i>He pulls out a knife, but doesn’t attack—yet.</i>\n\n"
            ">Hooded Man\n"
            "<b>\"Give me your stuff, and we all walk away happy. Say no, and I promise you won’t like what happens next.\"</b>\n\n" 
            ">Renji\n"
            "<b>\"Dude, this guy is sketchy as hell…\"</b>\n\n"
            ">CHOOSE YOUR RESPONSE\n"
            "<pre>Choice 1: Try To Talk Him Down\n"
            "Choice 2: Give Him Fake Wallet And Hopes He Buys It\n"
            "Choice 3: Attack First Before He Can</pre>",
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Choice 1",callback_data="c1s2o2_Talk"),
                  InlineKeyboardButton("Choice 2",callback_data="c1s2o2_Fake")],
                 [InlineKeyboardButton("Choice 3",callback_data="c1s2o2_Attack")]]
            )
        )
@app.on_callback_query(filters.regex(r"^(c1s2o|c1s2o2)_(\d+)$")) #c1s2o = chapter 1 scene 2 outcome
async def c1s2out(Client , CallbackQuery):
    data = CallbackQuery.data
    match = re.match(r"^(c1s2o|c1s2o2)_(\d+)$", data)
    data_state = database[CallbackQuery.message.from_user.id]
    if match:
        action = match.group(1)
        outcome = match.group(2)

    if action == "c1s2o":
        if outcome == "GiveMoney":
            asyncio.sleep(5)
            await CallbackQuery.message.delete()
            x=await Client.send_photo(
                CallbackQuery.message.chat.id,
                "https://files.catbox.moe/tgyolo.jpg",
                "<i>You handed over the money to the Hooded Man but it wasn't enough.\n"
                "As they turned away, he stabs them in their backs.</i>\n\n"
            )
            x.delete()
            await Client.send_photo(
                "",
                ""
            )
    if action == "c1s2o2":
        asyncio.sleep(5)
        await CallbackQuery.message.delete()
        try:
            if outcome == "Run":
                if random.random()<0.5:
                    res = await Client.send_photo(
                    "",
                    ""
                    )
                else:
                    data_state["status"] = "dead"
                    res = await Client.send_photo(
                    "",
                    ""
                    )
            elif outcome == "Stand":
                if random.random()<0.5:
                    res = await Client.send_photo(
                    "",
                    ""
                    )
                else:
                    data_state["status"] = "dead"
                    res = await Client.send_photo(
                    "",
                    ""
                    )
            elif outcome == "Fight":
                if random.random()<0.5:
                    res = await Client.send_photo(
                    "",
                    ""
                    )
                else:
                    data_state["status"] = "dead"
                    res = await Client.send_photo(
                    "",
                    ""
                    )
            elif outcome == "Distract":
                if random.random()<0.5:
                    res = await Client.send_photo(
                    "",
                    ""
                    )
                else:
                    data_state["status"] = "dead"
                    res = await Client.send_photo(
                    "",
                    ""
                    )
            elif outcome == "Esclate":
                if random.random()<0.5:
                    res = await Client.send_photo(
                    "",
                    ""
                    )
                else:
                    data_state["status"] = "dead"
                    res = await Client.send_photo(
                    "",
                    ""
                    )
            elif outcome == "Talk":
                if random.random()<0.5:
                    res = await Client.send_photo(
                    "",
                    ""
                    )
                else:
                    data_state["status"] = "dead"
                    res = await Client.send_photo(
                    "",
                    ""
                    )
            elif outcome == "Fake":
                if random.random()<0.5:
                    res = await Client.send_photo(
                    "",
                    ""
                    )
                else:
                    data_state["status"] = "dead"
                    res = await Client.send_photo(
                    "",
                    ""
                    )
            elif outcome == "Attack":
                if random.random()<0.5:
                    res = await Client.send_photo(
                    "",
                    ""
                    )
                else:
                    data_state["status"] = "dead"
                    res = await Client.send_photo(
                    "",
                    ""
                    )
        except Exception as e:
            print(e)
        finally:
            if database[CallbackQuery.message.from_user.id].get("status") == "dead":   
                asyncio.sleep(5)
                res.delete()
                res = await Client.send_photo(
                    "",
                    ""
                    )
                res.delete()
                await Client.send_photo(
                    "",
                    "",
                    reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Hide In Bushes",callback_data="c2r1")],
                    [InlineKeyboardButton("Call Out For Help",callback_data="c2r2")],
                    [InlineKeyboardButton("Run In Opposite Direction",callback_data="c2r3")]]
                    )
                )

@app.on_callback_query(filters.regex(r"^(c2r1|c2r2|c2r3)"))
async def ch2res(Client,CallbackQuery):
    data = CallbackQuery.data
    if data == "c2r1":
        await CallbackQuery.message.delete()
        await Client.send_photo(
            "",
            "",
            reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Hide In Bushes",callback_data="c2r1")],
                    [InlineKeyboardButton("Call Out For Help",callback_data="c2r2")],
                    [InlineKeyboardButton("Run In Opposite Direction",callback_data="c2r3")]]
                    )
        )
    if data == "c2r2":
        await CallbackQuery.message.delete()
        await Client.send_photo(
            "",
            "",
            reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Hide In Bushes",callback_data="c2r1")],
                    [InlineKeyboardButton("Call Out For Help",callback_data="c2r2")],
                    [InlineKeyboardButton("Run In Opposite Direction",callback_data="c2r3")]]
                    )
        )
    if data == "c2r3":
        await CallbackQuery.message.delete()
        await Client.send_photo(
            "",
            "",
            reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Hide In Bushes",callback_data="c2r1")],
                    [InlineKeyboardButton("Call Out For Help",callback_data="c2r2")],
                    [InlineKeyboardButton("Run In Opposite Direction",callback_data="c2r3")]]
                    )
        )

