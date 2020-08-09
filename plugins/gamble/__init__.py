from jieba import posseg
from nonebot import (CommandSession, IntentCommand, NLPSession, on_command,
                     on_natural_language)
from nonebot.permission import *

from utils_bot.typing import Callable, Generator, Union

from .diceroll import *

__plugin_name__ = '试试人品 *NL'
__plugin_usage__ = f'''feature: 生成随机数
可用命令：
扔骰子, 扔骰子 []次
扔硬币, 扔硬币 []次
'''

# help session
@on_command('试试人品', permission=GROUP_MEMBER | SUPERUSER)
async def try_luck(session: CommandSession):
    await session.send(__plugin_usage__)

class random_ops:
    @staticmethod
    async def evaluate(session: CommandSession, f: Callable):
        times: int = session.get('times')
        await session.send(f(**( {'times': times} if times else {} )))
    
    @staticmethod
    def nl_proc(session: NLPSession) -> Generator[Union[str, None], None, None]:
        argsStripped: str = session.msg_text.strip()
        words: Generator = posseg.lcut(argsStripped)

        for word in words:
            if word.flag == 'm':
                yield word.word
        yield None

@on_command('扔骰子', aliases=('扔色子', '扔个骰子', '扔个色子'), permission=GROUP_MEMBER | SUPERUSER)
async def roll_dice_host(session: CommandSession):
    await random_ops.evaluate(session, roll_dice_many)


@on_command('扔硬币', aliases=('扔个硬币', '扔钢镚', '扔个钢蹦'), permission=GROUP_MEMBER | SUPERUSER)
async def flip_coin_host(session: CommandSession):
    await random_ops.evaluate(session, flip_coin_many)



@roll_dice_host.args_parser
@flip_coin_host.args_parser
async def _(session: CommandSession):
    argsStripped: str = session.current_arg_text.strip(' \n次')
    session.state['times'] = argsStripped if argsStripped else None


# EXP
@on_natural_language(keywords={'骰子', '色子'}, permission=SUPERUSER | GROUP_MEMBER)
async def _(session: NLPSession):
    times = next(random_ops.nl_proc(session))
    return IntentCommand(64.0, '扔骰子', current_arg=times or None)

@on_natural_language(keywords={'硬币', '钢镚'}, permission=SUPERUSER | GROUP_MEMBER)
async def _(session: NLPSession):
    times = next(random_ops.nl_proc(session))
    return IntentCommand(64.0, '扔硬币', current_arg=times or None)
