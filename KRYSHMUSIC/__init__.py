# ======================================================
# ©️ 2025-26 All Rights Reserved by Krysh
# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : https://t.me/NexaCoders
# =======================================================

from KRYSHMUSIC.core.bot import Krysh
from KRYSHMUSIC.core.dir import dirr
from KRYSHMUSIC.core.git import git
from KRYSHMUSIC.core.userbot import Userbot
from KRYSHMUSIC.misc import dbb, heroku

from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Krysh()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

# ======================================================
# ©️ 2025-26 All Rights Reserved by Krysh
# 🧑‍💻 Developer : t.me/nonsecularman
# 🔗 Source link : https://github.com/devilcode-53/kryshMusic
# 📢 Telegram channel : https://t.me/NexaCoders
# =======================================================
