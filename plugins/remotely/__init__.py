from nonebot import CommandSession, on_command, get_bot
from nonebot.permission import *

__plugin_name__ = '遥控发送消息 (private)'
__plugin_usage__ = r'''feature: 遥控
    示例：
    发送到群 123456 内容
    发送到QQ 123456 内容
'''

class ops:
    @staticmethod
    async def send_to_x(session: CommandSession, msg_type: str):
        bot = get_bot()
        param = session.get('param')
        paramSplit = param.split(' ', 1)
        targetId, toSend = paramSplit[0], paramSplit[1]

        try:
            if msg_type == 'group':
                await bot.send_group_msg(group_id=targetId, message=toSend)
            elif msg_type == 'private':
                await bot.send_private_msg(user_id=targetId, message=toSend)
            await session.send('success!')
        except CQHttpError as exc:
            await session.send(str(exc))
    
    @staticmethod
    async def arg_parser_x(session: CommandSession):
        argStripped = session.current_arg.strip()
        if argStripped:
            session.state['param'] = argStripped
        else:
            await session.send('用法：\n发送到群/QQ [群号/QQ] [内容]')
            session.finish()

@on_command('发送到群', permission=SUPERUSER, privileged=True)
async def send_to_group(session: CommandSession):
    await ops.send_to_x(session, 'group')

@on_command('发送到QQ', permission=SUPERUSER, privileged=True)
async def send_to_private(session: CommandSession):
    await ops.send_to_x(session, 'private')

@send_to_group.args_parser
@send_to_private.args_parser
async def group_arg_parse(session: CommandSession):
    await ops.arg_parser_x(session)
