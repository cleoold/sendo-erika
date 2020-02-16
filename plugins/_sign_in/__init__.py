import random
from os import path

from nonebot import CommandSession, log, on_command, get_bot
from nonebot.permission import *

from utils_bot.typing import Tuple

from .execute import SignInSession, generate_luck_result

## this plugin overlaps with test_rp plugin
## 和 test_rp （今日运气）功能重合，欲启用此请先停用 test_rp 

__plugin_name__ = '签到/运气'
__plugin_usage__ = f'''feature: 要不要看一看自己的人品？
功能：签到，签到信息，今日运气
'''

SOME_GREETINGS = [
    '因为没办法才照顾你的哟，麻烦好好地感谢我一下！',
    '麻烦好好地照顾我一下！',
    '我是学院中最有人气的女生。',
    '要想获得本大小姐的青睐，可不是件容易的事噢？',
    '我——是——大——小——姐！',
    '请挺起胸膛、在这里我们才是主角！',
    '你知不知道、好奇心会杀死猫这句话？',
    '啊……嗯？',
    '呐，以后打算怎么办啊？',
    '不过算了。因为我现在心情很好。',
    '一，一大早的说什么呢你！',
    '谢，谢……',
    '好了，一鼓作气地上吧！',
    '星空好美啊',
    '人们会有点寂寞吧，那样子……',
    '为什么在发抖？',
    '呐，到底是哪里？',
    '如果会后悔的话，就不会来这里了。',
    '那也太凄凉了吧。我会花些心思的。'
]

SIGN_IN_DB_PATH = path.join(path.dirname(__file__), 'signin.db')

bot = get_bot()

# initialize db obsolete
@bot.server_app.before_serving
async def initialize_db():
    async with SignInSession(SIGN_IN_DB_PATH, 0, 0) as table_init:
        log.logger.debug('loading signin db...')
        await table_init.init_table()
        await table_init.commit()


def get_user_and_group_ids(session: CommandSession) -> Tuple[str, str]:
    user_id: str = session.ctx['user_id']
    group_id: str = session.ctx['group_id']
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
                f'{random.choice(SOME_GREETINGS)} 好感度：{score} (+{added})', 
                at_sender=True)
        else:
            await session.send(
                f'今日签到过啦~ 好感度：{score}', 
                at_sender=True)
    
    log.logger.debug(f'{user_id} trying to sign in in group {group_id} success: {status}')


@on_command('签到信息', aliases=('信息', 'signinfo'), permission=GROUP_MEMBER)
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
    senderId: int = int(session.ctx['user_id'])
    await session.send(generate_luck_result(senderId), at_sender=True)

