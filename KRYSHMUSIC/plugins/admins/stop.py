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
from KRYSHMUSIC.utils.database import set_loop
from KRYSHMUSIC.utils.decorators import AdminRightsCheck
from KRYSHMUSIC.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(
    filters.command(["end", "stop", "cend", "cstop"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return
    await Krysh.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_)
    )

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : t.me/nonsecularman
# =======================================================
