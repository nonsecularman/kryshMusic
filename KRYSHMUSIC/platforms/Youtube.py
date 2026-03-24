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
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pastebin.com/raw/rLsBhAQa") as res:
                if res.status == 200:
                    YOUR_API_URL = (await res.text()).strip()
                else:
                    YOUR_API_URL = FALLBACK_API_URL
    except:
        YOUR_API_URL = FALLBACK_API_URL


try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(load_api_url())
    else:
        loop.run_until_complete(load_api_url())
except:
    pass


async def download_song(link: str):
    return None


async def download_video(link: str):
    return None


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"

    async def exists(self, link: str):
        return bool(re.search(self.regex, link))

    # ✅ URL FIX
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

    # ✅ SAFE TRACK
    async def track(self, link: str, videoid: Union[bool, str] = None):
        try:
            if videoid:
                link = self.base + link

            results = VideosSearch(link, limit=1)
            data = await results.next()

            if not data or not data.get("result"):
                return None, None

            r = data["result"][0]

            return {
                "title": r.get("title"),
                "link": r.get("link"),
                "vidid": r.get("id"),
                "duration_min": r.get("duration"),
                "thumb": r.get("thumbnails")[0]["url"].split("?")[0]
                if r.get("thumbnails") else None,
            }, r.get("id")

        except:
            return None, None

    # ✅ SAFE DETAILS
    async def details(self, link: str):
        try:
            results = VideosSearch(link, limit=1)
            data = await results.next()

            if not data or not data.get("result"):
                return None, None, 0, None, None

            r = data["result"][0]

            return (
                r.get("title"),
                r.get("duration"),
                int(time_to_seconds(r.get("duration"))) if r.get("duration") else 0,
                r.get("thumbnails")[0]["url"].split("?")[0]
                if r.get("thumbnails") else None,
                r.get("id"),
            )
        except:
            return None, None, 0, None, None

    async def playlist(self, link, limit, *args):
        try:
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
        except:
            return None
