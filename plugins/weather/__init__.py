from nonebot import CommandSession, on_command, log
from nonebot.permission import *

from translate import Translator

from .data_source_amap import amap_weather
from .data_source_openweather import openweathermap_weather
from .china_city_list_source_amap import CHINESE_CITIES

__plugin_name__ = '天气'
__plugin_usage__ = r'''feature: 查询天气

天气 [城市]       获取天气预报
(source)
CN: AMAP, https://www.amap.com/
EN: openweathermap http://api.openweathermap.org/
'''

class util:
    @staticmethod
    def isChinese(word: str) -> bool:
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False
    
    @staticmethod
    def isAmapSupported(word: str) -> str:
        return word[:2] in CHINESE_CITIES
    
    @staticmethod
    def translate2Eng(word: str) -> str:
        # LOW EFFICIENCY MANUAL CORRECTION
        if word == '雪城': return 'syracuse'
        
        translator = Translator(from_lang='zh', to_lang='en')
        res = translator.translate(word).rstrip(' city')
        return res


@on_command('weather', aliases=('天气', '天气查询', '查询天气', '查天气'), permission=SUPERUSER | GROUP_MEMBER)
async def weather(session: CommandSession):
    city: str = session.get('city')
    isChinese: bool = util.isChinese(city)

    # AMAP
    if isChinese and util.isAmapSupported(city):
        weatherReport = await amap_weather(city)
    # OpenWeatherMap (delete block if you do not need)
    else:
        # openweathermap needs an English city name
        city = (city, util.translate2Eng(city))[isChinese]
        weatherReport = await openweathermap_weather(city)
    
    #log.logger.debug(city)
    await session.send(weatherReport)
    log.logger.debug(f'weather called: {weatherReport[:20]}...')

@weather.args_parser
async def _(session: CommandSession):
    argStripped: str = session.current_arg_text.strip()

    if session.is_first_run:
        if argStripped:
            session.state['city'] = argStripped
        else:
            session.finish(__plugin_usage__)