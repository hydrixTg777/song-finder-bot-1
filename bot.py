import os
import urllib
import requests
import subprocess
from requests import get

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_OWNER = int(os.environ["BOT_OWNER"])
DATABASE_URL = os.environ["DATABASE_URL"]
WOLFRAM_ID = os.environ.get("WOLFRAM_ID", None)


RSR = Client(
    "Answer Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START = """ Hi {}, I'm Answer Bot.\n\n
You can get answer for your question using me🙂
"""

ABOUT = """
● **OWNER :** [RSR](https://t.me/rsrmusic) 
● **SERVER :** `Heroku` 
● **LIBRARY :** `Pyrogram` 
● **LANGUAGE :** `Python 3.9` 
"""

HELP = """
Ask me something(i accpeted text only)
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('About',callback_data='rsrabout'),
        InlineKeyboardButton('Help',callback_data='rsrhelp')
        ],
        [
        InlineKeyboardButton('Join Channel', url='https://t.me/mizolibrary'),
        InlineKeyboardButton('Source', url='https://github.com/RSR-TG-Info/Join-Sticker'),
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
async def ask(bot, update):
    ques = urllib.parse.quote_plus(io)
    appid = WOLFRAM_ID
    server = f"https://api.wolframalpha.com/v1/spoken?appid={appid}&i={ques}"
    res = get(server)
    if "Wolfram Alpha did not understand" in res.text:
        await bot.send_chat_action(message.chat.id, "Typing")
        await bot.send_message(
            "**Sorry,i couldn't find answer for your question**😔"
        )
        return
    await bot.send_message(res.text, parse_mode="markdown")
