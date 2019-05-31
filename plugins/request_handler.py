from nonebot import (NoticeSession, RequestSession, get_bot, on_notice,
                     on_request)

__plugin_usage__ = r'''feature: 处理加群消息
'''

bot = get_bot()
SUPERUSERS = bot.config.SUPERUSERS

# accepts group invites only from superusers, instantly
@on_request('group.invite')
async def _(session: RequestSession):
    bot = get_bot()
    sender = session.ctx['user_id']
    if sender in SUPERUSERS:
        await session.approve()
        for eachId in SUPERUSERS:
            await bot.send_private_msg(user_id=eachId,
                message=f'接受了群{session.ctx["group_id"]}的邀请。(发起人：{sender})')
    else:
        await session.reject()


# notify superusers when bot joined a group
@on_notice('group_increase.invite')
async def _(session: NoticeSession):
    for eachId in SUPERUSERS:
        await bot.send_private_msg(user_id=eachId,
            message=f'加入了群{session.ctx["group_id"]}。')


# notify superusers when bot gets kicked from a group
@on_notice('group_decrease.kick_me')
async def _(session: NoticeSession):
    for eachId in SUPERUSERS:
        await bot.send_private_msg(user_id=eachId,
            message=f'被群{session.ctx["group_id"]}踢出了。')