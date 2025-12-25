# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : t.me/nonsecularman
# =======================================================

from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from KRYSHMUSIC import app
from KRYSHMUSIC.core.call import Krysh
from KRYSHMUSIC.utils import bot_sys_stats
from KRYSHMUSIC.utils.decorators.language import language
from KRYSHMUSIC.utils.inline import supp_markup
from KRYSHMUSIC.utils.inline import close_markup
from config import BANNED_USERS




@app.on_message(filters.command("ping", prefixes=["/", "!"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_video(
        video="https://files.catbox.moe/plxzb4.mp4",
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await Krysh.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : t.me/nonsecularman
# =======================================================
