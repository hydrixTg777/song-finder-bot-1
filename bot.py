import os
import urllib
import requests
import subprocess
import pyrogram
import io
from requests import get
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton




WOLFRAM_ID = os.environ.get("WOLFRAM_ID", None)


RSR = Client(
    "Answer Bot",
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

@RSR.on_message(filters.text & filters.private)
async def ask(client, message):
    ques = urllib.parse.quote_plus(str(io))
    appid = WOLFRAM_ID
    server = f"https://api.wolframalpha.com/v1/spoken?appid={appid}&i={ques}"
    chat_id = str(message.chat.id)
    res = get(server)
    await client.send_chat_action(message.chat.id, "Typing")
    await client.send_message(message.chat.id, res.text, parse_mode="markdown")
    if not res:
    await client.send_message(message.chat.id, "**Sorry,i couldn't find answer for your question😔**")


    
RSR.run()
	
