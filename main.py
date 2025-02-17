# (c) @AbirHasan2005 | Thomas Shelby
# This is Telegram Messages Forwarder UserBot!
# Use this at your own risk. I will not be responsible for any kind of issue while using this!

import os
import sys
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config
from helpers.kanger import Kanger
from helpers.forwarder import ForwardMessage

User = Client(session_name=Config.STRING_SESSION, api_hash=Config.API_HASH, api_id=Config.API_ID)


@User.on_message((filters.text | filters.media) & ~filters.edited)
async def main(client: Client, message: Message):
    if (Config.FORWARD_TO_CHAT_ID is None) or (Config.FORWARD_FROM_CHAT_ID is None):
        try:
            await client.send_message(chat_id="me",
                                      text=f"#VARS_MISSING: Please Set `FORWARD_FROM_CHAT_ID` or `FORWARD_TO_CHAT_ID` Config!")
        except FloodWait as e:
            await asyncio.sleep(e.x)
        return
    if (message.text == "!start") and (message.from_user.id == (await client.get_me()).id):
        await message.edit(text=f"Hi, **{(await client.get_me()).first_name}**!\nThis is a Forwarder Userbot by @sahil_nolia", parse_mode="Markdown",
                           disable_web_page_preview=True)
    elif (message.text == "!help") and (message.from_user.id == (await client.get_me()).id):
        await message.edit(
            text=Config.HELP_TEXT,
            parse_mode="Markdown", disable_web_page_preview=True)
    elif (message.text in ["!restart", "!stop"]) and (message.from_user.id == (await client.get_me()).id):
        if Config.HEROKU_APP is None:
            await message.edit(
                text="Restarting Userbot ...",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            # https://stackoverflow.com/a/57032597/15215201
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await message.edit(
                text="Restarting Heroku Dyno ..."
            )
            Config.HEROKU_APP.restart()
            time.sleep(30)
    elif (message.text == "!kang") and (message.from_user.id == (await client.get_me()).id):
        editable = await message.edit(
            text=f"Trying to Get All Messages from `{str(Config.FORWARD_FROM_CHAT_ID)}` and Forwarding to `{str(Config.FORWARD_TO_CHAT_ID)}` ...",
            parse_mode="Markdown", disable_web_page_preview=True)
        await asyncio.sleep(5)
        try_kang = await Kanger(c=User, m=editable)
        if try_kang == 400:
            return
    elif message.chat.id == (int(Config.FORWARD_FROM_CHAT_ID)):
        try_forward = await ForwardMessage(client, message)
        if try_forward == 400:
            return


User.run()
