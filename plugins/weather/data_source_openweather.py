# weather info source: openweathermap
#            tutorial: https://openweathermap.org/forecast5
# sample json fetch:
# http://api.openweathermap.org/data/2.5/forecast?appid=AAAAAAAAAAAAAAA&q=London&units=metric

from datetime import datetime
import json
import random

import aiohttp
from nonebot import get_bot

from utils_bot.typing import Union

#                                                      'weather' for current weather instead
URL_BASE: str = 'http://api.openweathermap.org/data/2.5/forecast?appid='
# +
API_KEY: str = get_bot().config.OPENWEATHERMAP_API_KEY
# +
URL_MODE: str = '&units=metric&cnt=25&q='
# +
#city

# fetch weather json data
async def fetch(*city: str) -> dict:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                    f'{URL_BASE}{API_KEY}{URL_MODE}{city[0]}',
                    headers=headers, timeout=10, ssl=False) as r:
                res = json.loads(await r.text())
                status = res['cod'].lower()
                assert status == '200' or status == '404'
                return res
        except BaseException:
            return None

# yields weather data
def process_weatherdata(resJson: Union[dict, None]) -> str:
    if resJson is None:
        return 'Temperature data unavailable'
    if not 'list' in resJson.keys():
        return '也许地址有误？'+\
            ('','如果这地址是对的，私聊我订正BUG！')[random.choice([0,0,1])]

    # location data
    cityChart: dict = resJson['city']
    nation = cityChart['country']
    city = cityChart['name'].upper()
    timezone = cityChart['timezone']
    reportTime = datetime.utcfromtimestamp(
        resJson['list'][0]['dt']).strftime('%Y-%m-%d %H:%M:%S')

    heading = f'''[below times are UTC]
region: {city}, {nation}, time diff from UTC: {timezone/60/60}h
  report time: {reportTime}\n'''

    def resGen():
        try:
            for j in range(0, 25, 4):
                directChart: dict = resJson['list'][j]
                mainChart = directChart['main']
                weatherChart = directChart['weather'][0]
                windChart = directChart['wind']
                # if tempMin and tempMax are same, only display one temp
                tempMin, tempMax = mainChart['temp_min'], mainChart['temp_max']
                temp = (f'{tempMin}-{tempMax}°C', f'{tempMin}°C')[tempMin == tempMax]
                yield \
f'''{directChart['dt_txt'][:16]}: {weatherChart['main']} ({weatherChart['description']}), {temp}
    wind: {windChart['speed']}m/s ({windChart['deg']}°), humidity: {mainChart['humidity']}, pressure: {mainChart['pressure']}hPa'''
        except (IndexError, KeyError):
            pass
    return heading + '\n'.join(resGen())

async def openweathermap_weather(*city: str):
    return process_weatherdata(await fetch(*city))
