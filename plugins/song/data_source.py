from urllib.parse import quote_plus

import aiohttp

from utils_bot.logging import logger
from utils_bot.typing import Union

# source: https://github.com/mixmoe/HibiAPI

URL_FORMAT = 'https://api.obfs.dev/api/netease/search?s={}&search_type=1&limit=1&offset=0'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

async def get_netease_song_id(name: str) -> Union[int, None]:
    try:
        async with aiohttp.ClientSession() as session:
            res = await session.get(URL_FORMAT.format(quote_plus(name)), headers=headers, timeout=10)
            res.raise_for_status()
            jsn = await res.json()
            return jsn['result']['songs'][0]['id']
    except Exception as e:
        logger.exception(e)
        return None
