from nonebot import CommandSession, log, on_command
from nonebot.permission import *

from utils_bot.command_ops import global_cooldown
from utils_bot.typing import depreciated

from .data_source import getGoogling

__plugin_name__ = 'google'
__plugin_usage__ = r'''feature: google search

google        获取前3条 google search 结果

DEPRECIATED
'''


@on_command('google', permission=SUPERUSER | GROUP_MEMBER)
@global_cooldown(40)
@depreciated
async def google(session: CommandSession):
    try:
        keyword = session.get('keyword')
        report = await getGoogling(keyword)
        await session.send(report)
        log.logger.debug(f'google search called: {report[:37]}...')
    except ValueError:
        await session.send('error')

@google.args_parser
@depreciated
async def _(session: CommandSession):
    paramStr = session.current_arg_text
    # if arg list is not empty
    if paramStr:
        session.state['keyword'] = paramStr.strip()
    else:
        session.finish(__plugin_usage__)
