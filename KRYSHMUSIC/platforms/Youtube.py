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
                    content = await response.text()
                    YOUR_API_URL = content.strip()
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
        if not YOUR_API_URL:
            YOUR_API_URL = FALLBACK_API_URL

    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link

    DOWNLOAD_DIR = "downloads"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")

    if os.path.exists(file_path):
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": video_id, "type": "audio"}

            async with session.get(
                f"{YOUR_API_URL}/download",
                params=params,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as response:
                if response.status != 200:
                    return None

                data = await response.json()
                token = data.get("download_token")

                if not token:
                    return None

                stream_url = f"{YOUR_API_URL}/stream/{video_id}?type=audio"

                async with session.get(
                    stream_url,
                    headers={"X-Download-Token": token},
                    timeout=aiohttp.ClientTimeout(total=300),
                ) as file_response:
                    if file_response.status != 200:
                        return None

                    with open(file_path, "wb") as f:
                        async for chunk in file_response.content.iter_chunked(16384):
                            f.write(chunk)

                    return file_path

    except Exception:
        return None


async def download_video(link: str) -> str:
    global YOUR_API_URL

    if not YOUR_API_URL:
        await load_api_url()
        if not YOUR_API_URL:
            YOUR_API_URL = FALLBACK_API_URL

    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link

    DOWNLOAD_DIR = "downloads"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

    if os.path.exists(file_path):
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": video_id, "type": "video"}

            async with session.get(
                f"{YOUR_API_URL}/download",
                params=params,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as response:
                if response.status != 200:
                    return None

                data = await response.json()
                token = data.get("download_token")

                if not token:
                    return None

                stream_url = f"{YOUR_API_URL}/stream/{video_id}?type=video"

                async with session.get(
                    stream_url,
                    headers={"X-Download-Token": token},
                    timeout=aiohttp.ClientTimeout(total=600),
                ) as file_response:
                    if file_response.status != 200:
                        return None

                    with open(file_path, "wb") as f:
                        async for chunk in file_response.content.iter_chunked(16384):
                            f.write(chunk)

                    return file_path

    except Exception:
        return None


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link

        results = VideosSearch(link, limit=1)
        data = await results.next()

        if not data["result"]:
            return None, None, 0, None, None

        result = data["result"][0]

        title = result["title"]
        duration = result.get("duration")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        vidid = result["id"]
        duration_sec = int(time_to_seconds(duration)) if duration else 0

        return title, duration, duration_sec, thumbnail, vidid

    async def title(self, link: str):
        results = VideosSearch(link, limit=1)
        data = await results.next()
        return data["result"][0]["title"]

    async def duration(self, link: str):
        results = VideosSearch(link, limit=1)
        data = await results.next()
        return data["result"][0].get("duration")

    async def thumbnail(self, link: str):
        results = VideosSearch(link, limit=1)
        data = await results.next()
        return data["result"][0]["thumbnails"][0]["url"].split("?")[0]

    async def track(self, link: str):
        results = VideosSearch(link, limit=1)
        data = await results.next()
        result = data["result"][0]

        return {
            "title": result["title"],
            "link": result["link"],
            "vidid": result["id"],
            "duration_min": result.get("duration"),
            "thumb": result["thumbnails"][0]["url"].split("?")[0],
        }, result["id"]

    async def playlist(self, link, limit):
        playlist = await Playlist.get(link)

        if not playlist:
            return None

        videos = []
        for video in playlist["videos"][:limit]:
            videos.append(
                {
                    "vidid": video["id"],
                    "title": video.get("title"),
                    "duration_min": video.get("duration"),
                }
            )

        return videos
