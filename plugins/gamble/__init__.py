from jieba import posseg
from nonebot import (CommandGroup, CommandSession, IntentCommand, NLPSession,
                     on_command, on_natural_language)
from nonebot.permission import *

from .diceroll import roll_dice, roll_dice_many

__plugin_name__ = '试试人品'
__plugin_usage__ = f'''feature: 生成随机数
可用命令：
扔骰子, 扔骰子 []次
'''

@on_command('扔骰子', aliases=('扔色子', '扔个骰子', '扔个色子'), permission=GROUP_MEMBER | SUPERUSER)
async def roll_dice_interface(session: CommandSession):
    times: int = session.get('times')
    if times == '':
        await session.send(roll_dice(pixel=True))
    else:
        await session.send(roll_dice_many(times))

@roll_dice_interface.args_parser
async def _(session: CommandSession):
    argsStripped: str = session.current_arg_text.strip(' \n次')
    session.state['times'] = argsStripped if argsStripped else ''
# EXP
@on_natural_language(keywords={'骰子', '色子'})
async def _(session: NLPSession):
    argsStripped = session.msg_text.strip()
    words = posseg.lcut(argsStripped)

    times = None
    for word in words:
        if word.flag == 'm':
            times = word.word

    return IntentCommand(66.0, '扔骰子', current_arg=times or '')
