from jieba import posseg
from nonebot import (CommandSession, IntentCommand, NLPSession,
                     on_command, on_natural_language)
from nonebot.permission import *
from translate import Translator

from utils_bot.logging import logger

from .china_city_list_source_amap import CHINESE_CITIES
from .data_source_amap import amap_weather
from .data_source_openweather import openweathermap_weather

__plugin_name__ = '天气 *NL'
__plugin_usage__ = r'''feature: 查询天气

天气 [城市]       获取天气预报
来源：
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
    def isAmapSupported(word: str) -> bool:
        return word.rstrip('市') in CHINESE_CITIES

    @staticmethod
    def translate2Eng(word: str) -> str:
        # LOW EFFICIENCY MANUAL CORRECTION
        if word == '雪城': return 'syracuse'

        translator = Translator(from_lang='zh', to_lang='en')
        res = translator.translate(word).lower().rstrip(' city')
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
        city = util.translate2Eng(city) if isChinese else city
        weatherReport = await openweathermap_weather(city)

    await session.send(weatherReport)
    logger.info(f'weather called: {weatherReport[:100]}...')

@weather.args_parser
async def _(session: CommandSession):
    argStripped: str = session.current_arg_text.strip()

    if session.is_first_run:
        if argStripped:
            session.state['city'] = argStripped
        else:
            session.finish(__plugin_usage__)
# EXP
@on_natural_language(keywords={'天气'}, permission=SUPERUSER | GROUP_MEMBER)
async def _(session: NLPSession):
    argsStripped = session.msg_text.strip()
    words = list(posseg.lcut(argsStripped))

    city = None
    for word in words:
        if word.flag == 'ns':
            city = word.word
            break
    if city is None:
        city = ' '.join((word.word for word in words if word.flag == 'eng'))

    return IntentCommand(64.0, 'weather', current_arg=city or '')
