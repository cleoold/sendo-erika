from datetime import datetime

import aiohttp
import bs4 # and lxml

from utils_bot.string_ops import my_ljust, my_rjust


# gets current time (server end)
def getTime() -> str:
    return datetime.now().strftime('%m-%d %H:%M:%S')

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
            soup = bs4.BeautifulSoup(await res.read(), features='lxml')

        titles = soup.select('.c-table.opr-toplist1-table a')           #|
        pops = soup.select('.opr-toplist1-right')                       #| place for updates
        length = len(titles)
        if length != len(pops) or length < 5: # one news matches one pop
            raise Exception('The number of entries don\'t match the number of popularities. Something must go wrong.')
        
        if opt != 'all':
            titles = titles[:6]
            pops = pops[:6]
            length = 6
        
        res = '     NEWS                  POP\n'
        for j in range(length):
            res += my_ljust(titles[j].getText(), 20) + my_rjust(pops[j].getText(), 10) + '\n'
        res += 'fetched %s with love. Source: www.baidu.com' % getTime()
        return res
    except Exception as exc:
        return exc # an error occurred
