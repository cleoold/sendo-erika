import re

from aiohttp import request
import bs4

from utils_bot.typing import depreciated

# 052219: adding browser headers creates cache in resulting page
_headers = { 
             'Cache-Control': 'private, max-age=0, no-cache',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip, deflate',
             'DNT': '1',
             'Connection': 'keep-alive',
             'Upgrade-Insecure-Requests': '1' }
_browser = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0' }

@depreciated
async def getGoogling(*keyword) -> str:
    header = _headers
    res = '>_< '
    try:
        count = 0
        linkElems, greenElems = [], []
        while len(linkElems) == 0:
            async with request(
                'GET', 'https://google.com/search?q=' + keyword[0], 
                headers=header) as resPage:
                soup = bs4.BeautifulSoup(await resPage.text(), features='lxml')

                # linkElems contains titles and GOOGLE URLS (without domain prefix)
                linkElems = soup.select('.r a')
                # greenElems contains displaying urls
                greenElems = soup.select('cite')
            count += 1
            if count == 10:
                header = dict(_headers, **_browser)
            elif count == 12:
                raise Exception('Google 好像此时不想让我们连接')

        displayLen = 3

        linkElems = linkElems[:3]
        greenElems = greenElems[:3]
        
    except Exception as exc:
        return str(exc)
    
    def parseOneGoogleUrl(gUrl) -> str:
        return re.search(r'q=(.+?\..+?)&[a-z]+=[A-Z]', gUrl).group(1)
    
    for j in range(displayLen):
        try:
            realUrl = parseOneGoogleUrl(linkElems[j].get('href'))
        except Exception:
            realUrl = greenElems[j].getText()
        res += linkElems[j].getText() + '\n' + realUrl + '\n'
    
    return res
