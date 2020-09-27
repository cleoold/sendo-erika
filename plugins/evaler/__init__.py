from nonebot import CommandSession, log, on_command
from nonebot.permission import *

from utils_bot.command_ops import global_cooldown

from .data_source_glot_run import SUPPORTED_LANGS, code_run_glot

__plugin_name__ = 'coderunner'
__plugin_usage__ = f'''feature: 执行代码

run [lang](这里空行)[statements]        执行语句
支持语言：{', '.join(SUPPORTED_LANGS.keys())}

示例：
run python
print(1+1)

attribution: https://glot.io
'''


@on_command('coderunner', aliases=('运行', '编译', 'run', 'exe'), permission=SUPERUSER | GROUP_MEMBER, only_to_me=False)
@global_cooldown(15)
async def coderunner(session: CommandSession):
    argsList: tuple = session.get('args')
    res = await code_run_glot(argsList[0], argsList[1])
    await session.send(res)
    log.logger.debug(f'coderunner called: {res[:20]}...')

@coderunner.args_parser
async def _(session: CommandSession):
    argsStripped: str = session.current_arg_text.strip()

    if session.is_first_run:
        if argsStripped:
            argsList: list = argsStripped.split('\n', 1)
            if len(argsList) < 2:
                session.finish(__plugin_usage__)

            lang, code = argsList[0].strip().lower(), argsList[1]
            #log.logger.debug(f'lang: {lang}, code:{code}')
            # manual correction
            if lang == 'py': lang = 'python'
            elif lang == 'c++': lang = 'cpp'
            elif lang == 'c#': lang = 'csharp'
            elif lang == 'js': lang = 'javascript'
            elif lang == 'f#': lang = 'fsharp'

            if not lang in SUPPORTED_LANGS.keys():
                session.finish('当前语言不支持~')

            session.state['args'] = (lang, code)
        else:
            session.finish(__plugin_usage__)
