import os
import asyncio
from shazamio import Shazam
from humanbyte import humanbytes
from pyrogram import filters, Client
import datetime
import requests
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from cmd import edit_or_reply, runcmd, fetch_audio


RSR = Client(
    "Audify Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START = """ Hi {}, I'm Song recogniser Bot.\n
**Tutorial** ⬇️\n
**Step 1** : Send me Video or Audio\n
**Step 2** : Reply your Video or Audio with this /audify command
"""

ABOUT = """
● **OWNER :** [RSR](https://t.me/rsrmusic) 
● **SERVER :** `Heroku` 
● **LIBRARY :** `Pyrogram` 
● **LANGUAGE :** `Python 3.8.6` 
"""

HELP = """
/audify : Reply Audio or Video\n
**+** When you have Deploy/Fork problem ask @rsrmusic
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
    await client.send_message(message.chat.id, text="`Processing...`", reply_to_message_id=message.message_id)
    if not message.reply_to_message:
        return await client.send_message(message.chat.id, text="**Reply Audio or Video.**", reply_to_message_id=message.message_id)
    if not (message.reply_to_message.audio or message.reply_to_message.voice or message.reply_to_message.video):
        return await client.send_message(message.chat.id, text="**Reply Audio or Video.**", reply_to_message_id=message.message_id)
    if message.reply_to_message.video:
        video_file = await message.reply_to_message.download()
        music_file = await convert_to_audio(video_file)
        dur = message.reply_to_message.video.duration
        if not music_file:
            return await client.send_message(message.chat.id, text="**Unable to convert to song file. Is this a valid file?**", reply_to_message_id=message.message_id)
    elif (message.reply_to_message.voice or message.reply_to_message.audio):
        dur = message.reply_to_message.voice.duration if message.reply_to_message.voice else message.reply_to_message.audio.duration
        music_file = await message.reply_to_message.download()
    size_ = humanbytes(os.stat(music_file).st_size)
    dur = datetime.timedelta(seconds=dur)
    thumb, by, title = await shazam(music_file)
    if title is None:
        return await client.send_message(message.chat.id, text="**Not found :(**", reply_to_message_id=message.message_id)
    etime = time.time()
    t_k = round(etime - stime)
    caption = f"""<b><u>Finded Song</b></u>
    
<b>Song Name :</b> <code>{title}</code>

<b>By :</b> <code>{by}</code>
    """
    if thumb:
        await msg.delete()
        await message.reply_to_message.reply_photo(thumb, caption=caption, quote=True)
    else:
        await msg.edit(caption)

    
RSR.run()
	
