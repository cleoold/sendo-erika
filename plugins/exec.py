import asyncio
import pprint
from typing import Awaitable, Callable

from nonebot import CommandSession, on_command
from nonebot.message import unescape
from nonebot.permission import *

from utils_bot.command_ops import force_private

__plugin_name__ = '远程执行 python (private)'
__plugin_usage__ = f'''feature: 执行代码
（根目录：bot.py文件所在目录）
remote [statements]
'''
# source: https://github.com/cczu-osa/aki/


@on_command('remote', permission=SUPERUSER)
@force_private
async def _(session: CommandSession):
    code = unescape(session.current_arg)

    try:
        localArgs = {}
        exec(code, None, localArgs)
        await session.send(f'Locals:\n{pprint.pformat(localArgs, indent=2)}')

        if isinstance(localArgs.get('run'), Callable):
            res = localArgs['run'](session.bot, session.event)
            if isinstance(res, Awaitable):
                res = await asyncio.wait_for(res, 6)
            await session.send(f'返回：\n{pprint.pformat(res, indent=2)}')
    except Exception as exc:
        await session.send(f'执行失败\n异常：\n{pprint.pformat(exc, indent=2)}')
