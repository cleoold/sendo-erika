from nonebot import CommandSession, on_command
from nonebot.permission import *

from utils_bot.command_ops import global_cooldown
from utils_bot.logging import logger

from .data_source import get_baidu_trend

__plugin_name__ = '百度热搜'
__plugin_usage__ = r'''feature: 百度热搜获取

百度热搜        获取前6条热搜
参数：
all            获取全部热搜
'''


@on_command('百度热搜', aliases=('百度热点', '时事新闻'), permission=SUPERUSER | GROUP_MEMBER)
@global_cooldown(40)
async def trend(session: CommandSession):
    arg = session.get('arg')
    trendReport = await get_baidu_trend(arg) # arg passed to function get_baidu_trend
    await session.send(trendReport)
    logger.info(f'Baidu trend called: {trendReport[32:37]}...')

@trend.args_parser
async def _(session: CommandSession):
    paramStr = session.current_arg_text
    # if arg list is not empty
    if paramStr:
        session.state['arg'] = paramStr.strip()
    else:
        session.state['arg'] = ''
