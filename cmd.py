import asyncio
import shlex
import time
from typing import Tuple
from bot import rsr1



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
        await rsr1.edit("**Reply Audio or Video🙄**")
        return
    warner_stark = message.reply_to_message
    if warner_stark.audio is None and warner_stark.video is None:
        await message.edit("**Format not Supported🤕**")
        return
    if warner_stark.video:
        await rsr1.edit("**Video Detected, Converting to Audio😊**")
        warner_bros = await message.reply_to_message.download(
            progress=progress, progress_args=(message, c_time, f"**Downloading Audio😁**")
        )
        stark_cmd = f"ffmpeg -i {warner_bros} -map 0:a friday.mp3"
        await runcmd(stark_cmd)
        final_warner = "friday.mp3"
    elif warner_stark.audio:
        await rsr1.edit("**Download Started🙃**")
        final_warner = await message.reply_to_message.download(
            progress=progress, progress_args=(message, c_time, f"**Downloading Video😁**`")
        )
    await rsr1.edit("**Almost Done🤭**")
    return final_warner
