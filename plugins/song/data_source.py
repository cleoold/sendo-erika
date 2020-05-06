import aiohttp

from utils_bot.typing import Union

# source: https://github.com/a632079/teng-koa

URL_BASE = 'https://v1.hitokoto.cn/nm/search/'
URL_PARAM = '?type=SONG&offset=0&limit=1'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

async def get_netease_song_id(name: str) -> Union[int, None]:
    try:
        async with aiohttp.ClientSession() as session:
            res = await session.get(f'{URL_BASE}{name}{URL_PARAM}', headers=headers, timeout=10)
            if res.status != 200:
                return None
            jsn = await res.json()
            return jsn['result']['songs'][0]['id']
    except Exception:
        return None
