import os
import urllib
import requests
import subprocess
from requests import get

from MashaRoBot.services.pyrogram import pbot
from pyrogram import filters
from MashaRoBot.pyrogramee.pluginshelper import edit_or_reply, get_text


WOLFRAM_ID = os.environ.get("WOLFRAM_ID", None)


@pbot.on_message(filters.command(["zawhna", "ask"]))
async def ask_friday(client, message):
    zote = await edit_or_reply(message, "`Typing...`")
    io = get_text(message)
    if not io:
        await zote.edit("Gimme Query🤨\n\n**Example👇**\n\n`/zawhna What is Atom?`")
        return
    ques = urllib.parse.quote_plus(io)
    appid = WOLFRAM_ID
    server = f"https://api.wolframalpha.com/v1/spoken?appid={appid}&i={ques}"
    res = get(server)
    if "Wolfram Alpha did not understand" in res.text:
        await zote.edit(
            "**Sorry,i couldn't recognized your question**\n\nI zawhna chhan na hi ka hmuzo lo😔"
        )
        return
    await zote.edit(res.text, parse_mode="markdown")
