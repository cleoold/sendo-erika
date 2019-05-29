from time import time

from nonebot import on_command, CommandSession, log
from nonebot.permission import *

from .data_source_glot_run import code_run_glot, SUPPORTED_LANGS

__plugin_name__ = 'coderunner'
__plugin_usage__ = f'''feature: 执行代码

run [lang](这里空行)[statements]        执行语句
支持语言：{', '.join(SUPPORTED_LANGS.keys())}

示例：
run python
print(1+1)

attribution: https://glot.io
'''

lastCall = time()

@on_command('coderunner', aliases=('运行', '编译', 'run', 'exe'), permission=SUPERUSER | GROUP_MEMBER, only_to_me=False)
async def coderunner(session: CommandSession):
    global lastCall
    if time() - lastCall > 15:
        argsList: str = session.get('args')

        res = await code_run_glot(argsList[0], argsList[1])
        await session.send(res)

        lastCall = time()
        log.logger.debug(f'coderunner called: {res[:20]}...')
    else:
        await session.send('技能冷却中……')

@coderunner.args_parser
async def _(session: CommandSession):
    argsStripped: str = session.current_arg_text.strip(' ')

    if session.is_first_run:
        if argsStripped:
            argsList: list = argsStripped.split('\n', 1)
            if len(argsList) < 2:
                session.finish()
            
            argv1, argv2 = argsList[0].strip().lower(), argsList[1]
            #log.logger.debug(f'argv1: {argv1}, argv2:{argv2}')
            # manual correction
            if argv1 == 'py': argv1 = 'python'
            if argv1 == 'c++': argv1 = 'cpp'
            if argv1 == 'c#': argv1 = 'csharp'

            if not argv1 in SUPPORTED_LANGS.keys():
                session.finish('当前语言不支持~')
            
            session.state['args'] = (argv1, argv2)
        else:
            session.finish(__plugin_usage__)