# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : t.me/nonsecularman
# =======================================================

from pyrogram import filters
from pyrogram.types import Message

from KRYSHMUSIC import app
from KRYSHMUSIC.core.call import Krysh

welcome = 20
close = 30


@app.on_message(filters.video_chat_started, group=welcome)
@app.on_message(filters.video_chat_ended, group=close)
async def welcome(_, message: Message):
    await Krysh.stop_stream_force(message.chat.id)

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : t.me/nonsecularman
# =======================================================
