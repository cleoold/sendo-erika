import nonebot
from nonebot import on_command, CommandSession, get_bot
from nonebot.permission import *

__plugin_name__ = '帮助'
__plugin_usage__ = r'''feature: 帮助

帮助        获取帮助
(with params)
[功能名]            获取特定功能的帮助
(example)
千堂帮助 google
'''

@on_command('帮助', aliases=['help', '功能'], permission=SUPERUSER | GROUP_MEMBER)
async def _(session: CommandSession):
    # get list of all plugins
    if session.event['user_id'] in get_bot().config.SUPERUSERS\
         and not session.event.get('group_id') \
         and not session.event.get('discuss_id'):
        plugins = [p for p in nonebot.get_loaded_plugins() if p.name]
    else:
        plugins = [p for p in nonebot.get_loaded_plugins() if p.name\
            and not p.name.endswith('private)')]

    arg = session.current_arg_text.strip().lower()
    if not arg:
        text = '呼叫我的名字来使用以下功能~:\n{\n\t' +\
            '\n\t'.join(p.name for p in plugins) + '\n}' +\
            '例子：帮助 天气'
        await session.send(text)

    else:
        for p in plugins:
            if arg in p.name.lower():
                await session.send(p.usage.strip())