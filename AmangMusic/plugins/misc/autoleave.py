#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
from datetime import datetime

import config
from AmangMusic import app
from AmangMusic.core.call import Amang, autoend
from AmangMusic.utils.database import (get_client, is_active_chat,
                                       is_autoend)


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT != str(True):
        return
    while not await asyncio.sleep(
            config.AUTO_LEAVE_ASSISTANT_TIME
        ):
        from AmangMusic.core.userbot import assistants

        for num in assistants:
            client = await get_client(num)
            left = 0
            try:
                async for i in client.iter_dialogs():
                    chat_type = i.chat.type
                    if chat_type in [
                            "supergroup",
                            "channel",
                        ]:
                        chat_id = i.chat.id
                        if chat_id not in [
                            config.LOG_GROUP_ID,
                            -1001284445583,
                            -1001772541015,
                        ]:
                            if left == 20:
                                continue
                            if not await is_active_chat(chat_id):
                                try:
                                    await client.leave_chat(
                                        chat_id
                                    )
                                    left += 1
                                except:
                                    continue
            except:
                pass


asyncio.create_task(auto_leave())


async def auto_end():
    while not await asyncio.sleep(5):
        if not await is_autoend():
            continue
        for chat_id in autoend:
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    continue
                autoend[chat_id] = {}
                try:
                    await Amang.stop_stream(chat_id)
                except:
                    continue
                try:
                    await app.send_message(
                        chat_id,
                        "ℹ️ Bot telah meninggalkan obrolan suara karena tidak aktif untuk menghindari kelebihan beban di server. Tidak ada yang mendengarkan bot di obrolan suara.",
                    )
                except:
                    continue


asyncio.create_task(auto_end())
