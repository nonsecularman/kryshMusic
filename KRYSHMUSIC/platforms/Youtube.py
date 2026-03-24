import asyncio
import os
import re
from typing import Union

import aiohttp
import yt_dlp
from youtubesearchpython import VideosSearch, Playlist
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

from KRYSHMUSIC import LOGGER
from KRYSHMUSIC.utils.formatters import time_to_seconds

YOUR_API_URL = None
FALLBACK_API_URL = "https://shrutibots.site"


async def load_api_url():
    global YOUR_API_URL
    logger = LOGGER("KRYSHMUSIC.platforms.Youtube.py")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://pastebin.com/raw/rLsBhAQa",
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 200:
                    YOUR_API_URL = (await response.text()).strip()
                    logger.info("API URL loaded successfully")
                else:
                    YOUR_API_URL = FALLBACK_API_URL
    except Exception:
        YOUR_API_URL = FALLBACK_API_URL


try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(load_api_url())
    else:
        loop.run_until_complete(load_api_url())
except RuntimeError:
    pass


async def download_song(link: str) -> str:
    global YOUR_API_URL

    if not YOUR_API_URL:
        await load_api_url()

    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link

    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{video_id}.mp3"

    if os.path.exists(file_path):
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": video_id, "type": "audio"}

            async with session.get(f"{YOUR_API_URL}/download", params=params) as res:
                data = await res.json()
                token = data.get("download_token")

            async with session.get(
                f"{YOUR_API_URL}/stream/{video_id}?type=audio",
                headers={"X-Download-Token": token},
            ) as file:
                with open(file_path, "wb") as f:
                    async for chunk in file.content.iter_chunked(1024):
                        f.write(chunk)

        return file_path
    except:
        return None


async def download_video(link: str) -> str:
    global YOUR_API_URL

    if not YOUR_API_URL:
        await load_api_url()

    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link

    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{video_id}.mp4"

    if os.path.exists(file_path):
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": video_id, "type": "video"}

            async with session.get(f"{YOUR_API_URL}/download", params=params) as res:
                data = await res.json()
                token = data.get("download_token")

            async with session.get(
                f"{YOUR_API_URL}/stream/{video_id}?type=video",
                headers={"X-Download-Token": token},
            ) as file:
                with open(file_path, "wb") as f:
                    async for chunk in file.content.iter_chunked(1024):
                        f.write(chunk)

        return file_path
    except:
        return None


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"

    async def exists(self, link: str):
        return bool(re.search(self.regex, link))

    # 🔥 FIXED URL METHOD
    async def url(self, message: Message):
        messages = [message]

        if message.reply_to_message:
            messages.append(message.reply_to_message)

        for msg in messages:
            if msg.entities:
                for entity in msg.entities:
                    if entity.type == MessageEntityType.URL:
                        text = msg.text or msg.caption
                        return text[entity.offset: entity.offset + entity.length]

            if msg.caption_entities:
                for entity in msg.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url

        return None

    async def details(self, link: str):
        results = VideosSearch(link, limit=1)
        data = await results.next()

        if not data["result"]:
            return None, None, 0, None, None

        r = data["result"][0]

        return (
            r["title"],
            r.get("duration"),
            int(time_to_seconds(r.get("duration"))) if r.get("duration") else 0,
            r["thumbnails"][0]["url"].split("?")[0],
            r["id"],
        )

    async def track(self, link: str):
        results = VideosSearch(link, limit=1)
        data = await results.next()
        r = data["result"][0]

        return {
            "title": r["title"],
            "link": r["link"],
            "vidid": r["id"],
            "duration_min": r.get("duration"),
            "thumb": r["thumbnails"][0]["url"].split("?")[0],
        }, r["id"]

    async def playlist(self, link, limit):
        data = await Playlist.get(link)

        if not data:
            return None

        return [
            {
                "vidid": v["id"],
                "title": v.get("title"),
                "duration_min": v.get("duration"),
            }
            for v in data["videos"][:limit]
        ]

    async def video(self, link: str):
        file = await download_video(link)
        return (1, file) if file else (0, "failed")

    async def download(self, link: str, video=False):
        file = await (download_video(link) if video else download_song(link))
        return (file, True) if file else (None, False)
