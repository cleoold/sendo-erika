from os import path

from nonebot import CommandSession, get_bot, log, on_command
from nonebot.permission import *

from utils_bot.typing import Tuple

from .execute import SignInSession, generate_luck_result
from .greets import get_greeting

## this plugin overlaps with test_rp plugin
## 和 test_rp （今日运气）功能重合，欲启用此请先停用 test_rp 

__plugin_name__ = '签到/运气'
__plugin_usage__ = f'''feature: 要不要看一看自己的人品？
功能：签到，签到信息，今日运气
'''


bot = get_bot()

SIGN_IN_DB_PATH = path.join(path.dirname(__file__), 'signin.db')

# initialize db obsolete
@bot.server_app.before_serving
async def initialize_db():
    async with SignInSession(SIGN_IN_DB_PATH, 0, 0) as table_init:
        log.logger.info('loading signin db...')
        await table_init.init_table()
        await table_init.commit()


def get_user_and_group_ids(session: CommandSession) -> Tuple[str, str]:
    user_id: str = session.event['user_id']
    group_id: str = session.event['group_id']
    return user_id, group_id


@on_command('签到', aliases=('sign',), permission=GROUP_MEMBER)
async def sign_in(session: CommandSession):
    try:
        user_id, group_id = get_user_and_group_ids(session)
    except KeyError:
        return
    async with SignInSession(SIGN_IN_DB_PATH, 
            user_id, group_id) as signin_session:
        await signin_session.init_user()
        status, score, added = await signin_session.user_sign_in()
        await signin_session.commit()
        if status:
            await session.send(
                f'{get_greeting(score)} 好感度：{score} (+{added})', 
                at_sender=True)
        else:
            await session.send(
                f'今日签到过啦~ 好感度：{score}', 
                at_sender=True)

    log.logger.debug(f'{user_id} trying to sign in in group {group_id} success: {status}')


@on_command('签到信息', aliases=('信息', 'signinfo', '好感度'), permission=GROUP_MEMBER)
async def check_sign_in_info(session: CommandSession):
    try:
        user_id, group_id = get_user_and_group_ids(session)
    except KeyError:
        return
    async with SignInSession(SIGN_IN_DB_PATH, 
        user_id, group_id) as signin_session:
        await signin_session.init_user()
        score, count, last = await signin_session.user_check()
        await session.send(
                    f'\n好感度：{score}\n历史签到次数：{count}\n上次签到：{last[4:]}.{last[:2]}.{last[2:4]}',
                    at_sender=True)


@on_command('我的运气', aliases=('运气', '今日运气', '今日人品', '我的人品', 'jrrp', '运势', '今日运势'), permission=GROUP_MEMBER | SUPERUSER)
async def my_luck_today(session: CommandSession):
    senderId: int = int(session.event['user_id'])
    await session.send(generate_luck_result(senderId), at_sender=True)

