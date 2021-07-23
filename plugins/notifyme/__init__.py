import re

from apscheduler.job import Job
from nonebot import (CommandSession, IntentCommand, MessageSegment, NLPSession,
                     get_bot, on_command, on_natural_language, scheduler)
from nonebot.permission import *

from utils_bot.datetime import TZ, datetime, timedelta
from utils_bot.logging import logger

__plugin_name__ = '定时提醒 *NL'
__plugin_usage__ = f'''feature: 在XX小时之后提醒用户
用法：
定时提醒 [H] [M] [信息]     我将在 H 时 M 分 后在本群发送信息提醒用户
取消定时提醒                撤销用户在本群设定的定时提醒
'''

MAX_HOURS = 25


def get_job_id(session: CommandSession) -> str:
    user = session.event['user_id']
    group = session.event.get('group_id', 0)
    return f'notifyme_qq{user}_grp{group}'


def fmt_job_scheduled_time(job: Job) -> str:
    return job.trigger.run_date.strftime('%m月%d日 %H:%M')


async def send_notify(user: int, msg: str, group:int=0):
    'group=0 means to send the message to private chat'
    bot = get_bot()
    if group != 0:
        sendmsg = MessageSegment.at(user) + ' ' + msg
        await bot.send_group_msg(group_id=group, message=sendmsg)
    else:
        await bot.send_private_msg(user_id=user, message=msg)
    logger.info(f'user {user} finished notifyme job in group {group}')


@on_command('定时提醒', aliases=('提醒我', '闹钟'), permission=GROUP_MEMBER | SUPERUSER)
async def notifyme_set(session: CommandSession):
    job_id = get_job_id(session)
    existing_job = scheduler.get_job(job_id)

    if existing_job:
        time = fmt_job_scheduled_time(existing_job)
        msg = existing_job.args[1]
        session.finish(f'您已有设定的定时提醒~\n{time} {msg} \n告诉我"取消定时提醒"来取消它')

    user, group = session.event['user_id'], session.event.get('group_id', 0)
    tdelta = session.get('tdelta')
    msg = session.get('msg')

    new_job = scheduler.add_job(send_notify, 'date',
        run_date=datetime.now(TZ) + tdelta,
        id=job_id,
        args=(user, msg, group)
    )

    time = fmt_job_scheduled_time(new_job)
    msg = new_job.args[1]
    await session.send(f'已设定：\n{time} {msg}')
    logger.info(f'user {user} finished notifyme job in group {group}')

@notifyme_set.args_parser
async def _(session: CommandSession):
    argsStripped = session.current_arg_text.strip() or ''
    args = argsStripped.split(' ', 2)

    if len(args) == 3:
        try:
            tdelta = timedelta(hours=int(args[0]), minutes=int(args[1]))
            if tdelta > timedelta(hours=MAX_HOURS) or tdelta < timedelta():
                session.finish(f'最多只能设定到{MAX_HOURS}小时~')
            session.state['tdelta'] = tdelta
            session.state['msg'] = args[2]
        except (ValueError, IndexError):
            session.finish(__plugin_usage__)
    else:
        session.finish(__plugin_usage__)

@on_natural_language(keywords={'提醒我'}, permission=SUPERUSER | GROUP_MEMBER)
async def _(session: NLPSession):
    sentence = session.msg_text.strip().replace('提醒我', '', 1)

    def r(regex):
        search = re.findall(regex, sentence)
        return search[0] if search != [] else search

    # re.findall(regex,'5小时3分钟后(提醒我)xxxxxyyy') 
    # -> [('5小时', '5', '小时', '3分钟', '3', '分钟', 'xxxxxyyy')]
    search = r(r'((\d+) ?(小?时|h|H))? ?((\d+) ?(分钟?|min))?后?(.+)$')
    if len(search) == 7 and (search[1] or search[4]):
        return IntentCommand(64.0, '定时提醒', current_arg=f'{search[1] or 0} {search[4] or 0} {search[6]}')
    # re.findall(regex, '13:42后xxxx')
    # -> [('13', '42', 'xxxx')]
    search = r(r'(\d{1,2}):(\d{1,2}) ?后(.+)$')
    if len(search) == 3:
        return IntentCommand(64.0, '定时提醒', current_arg=f'{search[0]} {search[1]} {search[2]}')
    # re.findall(regex, '13:42xxxx')
    # -> [('13', ':', '42', 'xxxx')]
    # TODO: this part is improvable
    search = r(r'(\d{2})(:|点)(\d{2}) ?(.+)$')
    if len(search) == 4:
        now = datetime.now(TZ)
        dt = (now.replace(hour=int(search[0]), minute=int(search[2]),
            second=0, microsecond=0) - now).total_seconds()
        return IntentCommand(64.0, '定时提醒', current_arg=f'0 {int(dt/60)+1} {search[3]}')

    return IntentCommand(0, '定时提醒')


@on_command('取消定时提醒', aliases=('撤销定时提醒',), permission=GROUP_MEMBER | SUPERUSER)
async def notifyme_revoke(session: CommandSession):
    job = scheduler.get_job(get_job_id(session))
    if job:
        time = fmt_job_scheduled_time(job)
        job.remove()
        await session.send(f'已取消预定于 {time} 的定时提醒')
    else:
        await session.send('您没有设定定时提醒~')
