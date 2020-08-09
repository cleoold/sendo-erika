from nonebot import CommandSession, get_bot, load_plugins, on_command
from nonebot.exceptions import CQHttpError
from nonebot.message import unescape
from nonebot.permission import *

from utils_bot.typing import depreciated

__plugin_name__ = '遥控机器人 (private)'
__plugin_usage__ = r'''feature: 遥控
发送消息：
发送到群 [群号] [内容]
发送到QQ [QQ号] [内容]

发送CQ码：
发送到群CQ [群号] [内容]
发送到QQCQ [QQ号] [内容]

改群名片：
改群名片 [群号] [内容 | '']  （内容为空代表删除）

查看已加入的群：
所在的群
'''

async def send_to_x(session: CommandSession, msg_type: str, unescape_=False):
    bot = get_bot()
    targetId, toSend = session.get('id'), session.get('msg')
    if unescape_:
        toSend = unescape(toSend)

    try:
        if msg_type == 'group':
            await bot.send_group_msg(group_id=targetId, message=toSend)
        elif msg_type == 'private':
            await bot.send_private_msg(user_id=targetId, message=toSend)
        await session.send('success!')
    except CQHttpError as exc:
        await session.send(str(exc))

@on_command('发送到群', permission=SUPERUSER, privileged=True)
async def send_to_group(session: CommandSession):
    await send_to_x(session, 'group')

@on_command('发送到QQ', permission=SUPERUSER, privileged=True)
async def send_to_private(session: CommandSession):
    await send_to_x(session, 'private')

@on_command('发送到群CQ', permission=SUPERUSER, privileged=True)
async def send_to_group_CQ(session: CommandSession):
    await send_to_x(session, 'group', True)

@on_command('发送到QQCQ', permission=SUPERUSER, privileged=True)
async def send_to_private_CQ(session: CommandSession):
    await send_to_x(session, 'private', True)

@send_to_group_CQ.args_parser
@send_to_private_CQ.args_parser
@send_to_group.args_parser
@send_to_private.args_parser
async def _(session: CommandSession):
    argStripped = session.current_arg.strip() or ''
    args = argStripped.split(' ', 1)
    if len(args) == 2:
        session.state['id'] = args[0]
        session.state['msg'] = args[1]
    else:
        session.finish('用法：\n发送到群/QQ [群号/QQ] [内容]')


@on_command('改群名片', permission=SUPERUSER, privileged=True)
async def change_my_group_card(session: CommandSession):
    bot = get_bot()
    targetId, card = session.get('id'), session.get('card')
    try:
        await bot.set_group_card(group_id=targetId, user_id=bot.config.SELF_QQ, card=card)
        await session.send('success!')
    except CQHttpError as exc:
        await session.send(str(exc))

@change_my_group_card.args_parser
async def _(session: CommandSession):
    argStripped = session.current_arg.strip() or ''
    args = argStripped.split(' ', 1) if argStripped else []
    if len(args) >= 1:
        session.state['id'] = args[0]
        session.state['card'] = args[1] if len(args) >= 2 else ''
    else:
        session.finish('用法：\n改群名片 [群号] [内容 | ""]')


@on_command('所在的群', permission=SUPERUSER, privileged=True)
async def groups_in(session: CommandSession):
    groups: dict = await get_bot().get_group_list()
    res = ''
    for each in groups:
        res += f'{each["group_id"]}: {each["group_name"]}\n'
    res = res.rstrip('\n')
    await session.send(res)


@on_command('重置插件', permission=SUPERUSER, privileged=True)
@depreciated
async def reset_plugins(session: CommandSession):
    from os import path
    load_plugins(path.join('.', 'plugins'), 'plugins')
