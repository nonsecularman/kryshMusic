# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : t.me/nonsecularman
# =======================================================

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from KRYSHMUSIC import app

@app.on_message(filters.command("privacy"))
async def privacy_command(client: Client, message: Message):
    await message.reply_photo(
        photo="https://files.catbox.moe/raxhof.jpg",
        caption="**➻ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴋʀɪᴛɪ ʙᴏᴛѕ ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴄʏ.**\n\n**⊚ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛʜᴇɴ ꜱᴇᴇ ʙᴏᴛs ᴘʀɪᴠᴧᴄʏ ᴘᴏʟɪᴄʏ 🔏**",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ᴘʀᴏᴍᴏ", url="https://t.me/nonsecularman?text=𝖧ᴇʏ%20ʙᴀʙʏ%20%20😄%20ɪ%20ᴡᴀɴᴛ%20ᴘᴀɪᴅ%20ᴘʀᴏᴍᴏᴛɪᴏɴ,%20ɢɪᴠᴇ%20ᴍᴇ%20ᴘʀɪᴄᴇ%20ʟɪsᴛ%20😙")]
            ]
        )
    )

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : t.me/nonsecularman
# =======================================================
