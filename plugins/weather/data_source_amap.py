# weather info source: amap
#            tutorial: https://lbs.amap.com/api/webservice/guide/api/weatherinfo/
# sample json fetch:
# http://restapi.amap.com/v3/weather/weatherInfo?key=AAAAAAAAAAAAA&city=%E6%BE%B3%E9%97%A8&extensions=all

import json
import re

import aiohttp
from nonebot import get_bot

from utils_bot.typing import Union

URL_BASE: str = 'http://restapi.amap.com/v3/weather/weatherInfo?key='
# +
API_KEY: str = get_bot().config.AMAP_WEATHER_API_KEY
# +
URL_MODE: str = '&extensions=all&city='
# +
# city

# fetch weather json data
async def fetch(city: str) -> Union[dict, None]:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                    f'{URL_BASE}{API_KEY}{URL_MODE}{city}',
                    headers=headers, timeout=10, ssl=False) as r:
                res = json.loads(await r.text(), encoding='utf-8')
                assert res['info'].lower() == 'ok'
                return res
        except Exception:
            return None

# yields weather data
def process_weatherdata(resJson: Union[dict, None]) -> str:
    if resJson is None:
        return '天气服务不可用'
    
    if not resJson['forecasts']:
        return '也许地址有误？'
    # location data
    province = resJson['forecasts'][0]['province']
    city = resJson['forecasts'][0]['city']
    time = resJson['forecasts'][0]['reporttime']

    heading = f'预报时间：{time}\n地区：{province} {city}\n'
    def process_wind_str(wind: str) -> str:
        # possible wind input: '东北', '无风'
        return wind + '风' if re.search(r'东|南|西|北', wind) else wind
    def resGen():
        try:
            for j in range(3):
                locCurrDay = resJson['forecasts'][0]['casts'][j]
                yield \
f'''{locCurrDay['date']} 日：{locCurrDay['daytemp']}°C，{locCurrDay['dayweather']}，{process_wind_str(locCurrDay['daywind'])}
{locCurrDay['date']} 夜：{locCurrDay['nighttemp']}°C，{locCurrDay['nightweather']}，{process_wind_str(locCurrDay['nightwind'])}'''
        except (IndexError, KeyError):
            pass
    return heading + '\n'.join(resGen())

async def amap_weather(city: str):
    return process_weatherdata(await fetch(city))
