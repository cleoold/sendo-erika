from time import time

from nonebot import CommandSession, on_command, log
from nonebot.permission import *

from utils_bot.typing import depreciated

from .data_source import getGoogling

__plugin_name__ = 'google'
__plugin_usage__ = r'''feature: google search

google        获取前3条 google search 结果

DEPRECIATED
'''

lastCall = time()
COOLDOWN = 40

@on_command('google', permission=SUPERUSER | GROUP_MEMBER)
@depreciated
async def google(session: CommandSession):
    global lastCall
    if time() - lastCall > COOLDOWN:
        try:
            keyword = session.get('keyword')
            report = await getGoogling(keyword)
            await session.send(report)
            lastCall = time()
            log.logger.debug(f'google search called: {report[:37]}...')
        except ValueError:
            await session.send('error')
    else:
        await session.send(f'技能冷却中…… ({COOLDOWN}s)')

@google.args_parser
@depreciated
async def _(session: CommandSession):
    paramStr = session.current_arg_text
    # if arg list is not empty
    if paramStr:
        session.state['keyword'] = paramStr.strip()
    else:
        session.finish(__plugin_usage__)
