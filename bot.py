import os
import asyncio
from shazamio import Shazam
from humanbyte import humanbytes
from pyrogram import filters, Client
import datetime
import requests
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from cmd import runcmd, fetch_audio


RSR = Client(
    "Audify Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START = """ Hi {}, I'm recogniser Bot.\n
You can find some video/audio 🙂
"""

ABOUT = """
● **OWNER :** [RSR](https://t.me/rsrmusic) 
● **SERVER :** `Heroku` 
● **LIBRARY :** `Pyrogram` 
● **LANGUAGE :** `Python 3.9` 
"""

HELP = """
/audify : Reply Audio or Video
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('About',callback_data='rsrabout'),
        InlineKeyboardButton('Help',callback_data='rsrhelp')
        ],
        [
        InlineKeyboardButton('Channel', url='https://t.me/mizolibrary'),
        InlineKeyboardButton('Source', url='https://github.com/RSR-TG-Info/song-finder-bot'),
        ],
        [InlineKeyboardButton('Owner', url="t.me/rsrmusic")
        ]]
        
    )
BACK_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Back',callback_data='rsrback'),
        ]]
    )

@RSR.on_callback_query()
async def cb_data(bot, update):  
    if update.data == "rsrhelp":
        await update.message.edit_text(
            text=HELP,
            reply_markup=BACK_BTN,
            disable_web_page_preview=True
        )
    elif update.data == "rsrabout":
        await update.message.edit_text(
            text=ABOUT,
            disable_web_page_preview=True,
            reply_markup=BACK_BTN
	)
    else:
        await update.message.edit_text(
            text=START.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BTN
        )
        
@RSR.on_message(filters.command(["start"]) & filters.private)
async def start(bot, update):
    text = START.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@RSR.on_message(filters.command(["audify"]))
async def shazamm(client, message):
    rsr1 = await message.reply_text("⏳")
    if not message.reply_to_message:
        await rsr1.edit("Reply Audio or Video.")
        return
    if os.path.exists("friday.mp3"):
        os.remove("friday.mp3")
    kkk = await fetch_audio(client, message)
    downloaded_file_name = kkk
    f = {"file": (downloaded_file_name, open(downloaded_file_name, "rb"))}
    await rsr1.edit("🔍")
    r = requests.post("https://starkapi.herokuapp.com/shazam/", files=f)
    try:
        xo = r.json()
    except JSONDecodeError:
        await rsr1.edit("`Song not found😔`")
        return
    if xo.get("success") is False:
        await rsr1.edit("`Song not found😔`")
        os.remove(downloaded_file_name)
        return
    xoo = xo.get("response")
    zz = xoo[1]
    zzz = zz.get("track")
    if not zzz:
        await rsr1.edit("`Song not found😔`")
        return
    nt = zzz.get("images")
    image = nt.get("coverarthq")
    by = zzz.get("subtitle")
    title = zzz.get("title")
    messageo = f"""<b><u>Identify Finished ✅</b></u>\n
<b>📁 Song Name : </b> {title}\n
<b>🎙️ Artist : </b>{by}
"""
    await client.send_photo(message.chat.id, image, messageo, reply_to_message_id=message.reply_to_message.message_id, parse_mode="HTML")
    os.remove(downloaded_file_name)
    await kek.delete()

    
RSR.run()
	
