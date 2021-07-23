import aiohttp
import bs4  # and lxml

from utils_bot.datetime import TZ, datetime
from utils_bot.logging import logger


# gets current time
def getTime() -> str:
    return datetime.now(TZ).strftime('%m-%d %H:%M:%S')

# a page that always works for the program purpose 
url: str = "https://www.baidu.com/s?wd=sousuoredian"
headers: dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    # 'Cookie': 'sometimes you need this'
}

async def get_baidu_trend(opt: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            res = await session.get(url, headers=headers, timeout=3)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(await res.read(), features='lxml')

        titles = soup.select('a.opr-toplist1-subtitle')           #|
        #pops = soup.select('.opr-toplist1-right')                #| place for updates
        length = len(titles)

        if opt != 'all':
            length = 6

        res = '     NEWS\n'
        for j in range(length):
            res += titles[j].getText().strip() + '\n'
        res += 'fetched %s with love. Source: www.baidu.com' % getTime()
        return res
    except Exception as e:
        logger.exception(e)
        return 'an error occurred'
