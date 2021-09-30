import asyncio
import shlex
import time
from typing import Tuple
from pyrogram.types import Message
from pyrogram import Client


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def fetch_audio(client, message):
    """Fetch Audio From Videos Or Audio Itself"""
    c_time = time.time()
    if not message.reply_to_message:
        message.reply("**Reply Audio or Video🙄**")
        return
    warner_stark = message.reply_to_message
    if warner_stark.audio is None and warner_stark.video is None:
        await message.reply("**Format not Supported🤕**")
        return
    if warner_stark.video:
        rsr2 = await message.reply("**Converting to Audio😊**")
        warner_bros = await message.reply_to_message.download(
            progress=progress, progress_args=(message, c_time, f"**Downloading Audio😁**")
        )
        stark_cmd = f"ffmpeg -i {warner_bros} -map 0:a friday.mp3"
        await runcmd(stark_cmd)
        final_warner = "friday.mp3"
    elif warner_stark.audio:
        rsr2 = await edit_or_reply("**Download Started🙃**")
        final_warner = await message.reply_to_message.download(
            progress=progress, progress_args=(message, c_time, f"**Downloading Video😁**`")
        )
    await rsr2.edit("**Almost Done🤭**")
    await rsr2.delete()
    return final_warner


async def edit_or_reply(message, text, parse_mode="md"):
    if message.from_user.id:
        if message.reply_to_message:
            kk = message.reply_to_message.message_id
            return await message.reply_text(
                text, reply_to_message_id=kk, parse_mode=parse_mode
            )
        return await message.reply_text(text, parse_mode=parse_mode)
    return await message.edit(text, parse_mode=parse_mode)
