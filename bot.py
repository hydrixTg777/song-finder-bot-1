import os
import asyncio
from shazamio import Shazam
from humanbyte import humanbytes
from pyrogram import filters, Client
import datetime
import requests
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


RSR = Client(
    "Audify Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START = """ Hi {}, I'm Answer Bot.\n
You can get answer for your question using me🙂
"""

ABOUT = """
● **OWNER :** [RSR](https://t.me/rsrmusic) 
● **SERVER :** `Heroku` 
● **LIBRARY :** `Pyrogram` 
● **LANGUAGE :** `Python 3.9` 
"""

HELP = """
Ask me something(Text only)
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('About',callback_data='rsrabout'),
        InlineKeyboardButton('Help',callback_data='rsrhelp')
        ],
        [
        InlineKeyboardButton('Channel', url='https://t.me/mizolibrary'),
        InlineKeyboardButton('Source', url='https://github.com/RSR-TG-Info/Answer-Bot'),
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



async def shazam(file):
    shazam = Shazam()
    try:
        r = await shazam.recognize_song(file)
    except:
        return None, None, None
    if not r:
        return None, None, None
    track = r.get("track")
    nt = track.get("images")
    image = nt.get("coverarthq")
    by = track.get("subtitle")
    title = track.get("title")
    return image, by, title

async def convert_to_audio(vid_path):
    stark_cmd = f"ffmpeg -i {vid_path} -map 0:a friday.mp3"
    await runcmd(stark_cmd)
    final_warner = "friday.mp3"
    if not os.path.exists(final_warner):
        return None
    return final_warner

@RSR.on_message(filters.command(["audify"]))
async def shazam_(client, message):
    stime = time.time()
    rsr1 = await message.reply_text("🔍")
    if not message.reply_to_message:
        return await rsr1.edit("`Reply Audio or Video`")
    if not (message.reply_to_message.audio or message.reply_to_message.voice or message.reply_to_message.video):
        return await rsr1.edit("`Reply to Audio File`")
    if message.reply_to_message.video:
        video_file = await message.reply_to_message.download()
        music_file = await convert_to_audio(video_file)
        dur = message.reply_to_message.video.duration
        if not music_file:
            return await rsr1.edit("`Unable to convert to Song File. Is this a valid File?`")
    elif (message.reply_to_message.voice or message.reply_to_message.audio):
        dur = message.reply_to_message.voice.duration if message.reply_to_message.voice else message.reply_to_message.audio.duration
        music_file = await message.reply_to_message.download()
    size_ = humanbytes(os.stat(music_file).st_size)
    dur = datetime.timedelta(seconds=dur)
    thumb, by, title = await shazam(music_file)
    if title is None:
        return await rsr1.edit("`No results found`")
    etime = time.time()
    t_k = round(etime - stime)
    caption = f"""<b><u>Identified Finish ✅</b></u>
    
<b>📂Song Name :</b> <code>{title}</code>
<b>🎙️Artist :</b> <code>{by}</code>
<b>⏳Duration :</b> <code>{dur}</code>
<b>🗂️Size :</b> <code>{size_}</code>
<b>⏰Time Taken :</b> <code>{t_k} Seconds</code>
    """
    if thumb:
        await rsr1.delete()
        await message.reply_to_message.reply_photo(thumb, caption=caption, quote=True)
    else:
        await rsr1.edit(caption)

    
RSR.run()
	
