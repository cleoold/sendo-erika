from time import time

from nonebot import CommandSession, on_command, log
from nonebot.permission import *

from .data_source import getbaiduTrend

__plugin_name__ = '百度热搜获取'
__plugin_usage__ = r'''feature: 百度热搜获取

百度热搜        获取前6条热搜
(with params)
all            获取全部热搜
'''

lastCall = time()
COOLDOWN = 40

@on_command('百度热搜', aliases=('百度热点', '时事新闻'), permission=SUPERUSER | GROUP_MEMBER)
async def trend(session: CommandSession):
    global lastCall
    if time() - lastCall > COOLDOWN:
        arg = session.get('arg')
        trendReport = await getbaiduTrend(arg) # arg passed to function getbaiduTrend
        await session.send(trendReport)
        lastCall = time()
        log.logger.debug(f'Baidu trend called: {trendReport[32:37]}...')
    else:
        await session.send(f'技能冷却中…… ({COOLDOWN}s)')

@trend.args_parser
async def _(session: CommandSession):
    paramStr = session.current_arg_text
    # if arg list is not empty
    if paramStr:
        session.state['arg'] = paramStr.strip()
    else:
        session.state['arg'] = ''
