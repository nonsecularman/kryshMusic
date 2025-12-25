# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : t.me/nonsecularman
# =======================================================

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message

from KRYSHMUSIC import app
from KRYSHMUSIC.utils.database import get_playmode, get_playtype, is_nonadmin_chat
from KRYSHMUSIC.utils.decorators import language
from KRYSHMUSIC.utils.inline.settings import playmode_users_markup
from config import BANNED_USERS


@app.on_message(filters.command(["playmode" , "mode" ] ,prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.group & ~BANNED_USERS)
@language
async def playmode_(client, message: Message, _):
    playmode = await get_playmode(message.chat.id)
    if playmode == "Direct":
        Direct = True
    else:
        Direct = None
    is_non_admin = await is_nonadmin_chat(message.chat.id)
    if not is_non_admin:
        Group = True
    else:
        Group = None
    playty = await get_playtype(message.chat.id)
    if playty == "Everyone":
        Playtype = None
    else:
        Playtype = True
    buttons = playmode_users_markup(_, Direct, Group, Playtype)
    response = await message.reply_text(
        _["play_22"].format(message.chat.title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : t.me/nonsecularman
# =======================================================
