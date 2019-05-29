import sys as _sys
from datetime import datetime

import bs4 as _bs4 #and lxml
import aiohttp as _aiohttp


# fixes aligning problems for multibyte characters
def _ljust(s, n): return s.ljust(n - (len(s.encode("gbk")) - len(s)))
def _rjust(s, n): return s.rjust(n - (len(s.encode("gbk")) - len(s)))

# gets current time (server end)
def getTime() -> str:
    return datetime.now().strftime('%m-%d %H:%M:%S')

# a page that always works for the program purpose 
_url: str = "https://www.baidu.com/s?wd=sousuoredian"
_headers: dict = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' }

async def getbaiduTrend(*args) -> str:
    try:
        async with _aiohttp.ClientSession() as session:
            res = await session.get(_url, headers=_headers, timeout=3, ssl=False)
            soup = _bs4.BeautifulSoup(await res.read(), features='lxml')

        titles = soup.select('td table tbody tr td span a')           #|
        pops = soup.select('td table tbody tr .opr-toplist1-right')   #| place for updates
        length = len(titles)
        if length != len(pops) or length < 5: # one news matches one pop
            raise Exception('The number of entries don\'t match the number of popularities. Something must go wrong.')
        
        if args[0] != 'all':
            titles = titles[:6]
            pops = pops[:6]
            length = 6
        
        res = '     NEWS                  POP\n'
        for j in range(length):
            res += _ljust(titles[j].getText(), 20) + _rjust(pops[j].getText(), 10) + '\n'
        res += 'fetched %s with love. Source: www.baidu.com' % getTime()
        return res
    except Exception as exc:
        return exc # an error occurred

