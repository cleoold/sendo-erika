from nonebot import NoticeSession, RequestSession, on_notice, on_request

from utils_bot.msg_ops import SUPERUSERS, send_to_superusers

__plugin_usage__ = r'''feature: 处理群消息
'''



# accepts group invites only from superusers, instantly
@on_request('group.invite')
async def _(session: RequestSession):
    sender = session.ctx['user_id']
    if sender in SUPERUSERS:
        await session.approve()
        await send_to_superusers(
            f'接受了群{session.ctx["group_id"]}的邀请。(发起人：{sender})')
    else:
        await session.reject()


# notify superusers when bot joins a group
@on_notice('group_increase.invite')
async def _(session: NoticeSession):
    if session.ctx['self_id'] != session.ctx['user_id']:
        return
    await send_to_superusers(
        f'加入了群{session.ctx["group_id"]}。')


# notify superusers when bot gets kicked from a group
@on_notice('group_decrease.kick_me')
async def _(session: NoticeSession):
    if session.ctx['self_id'] != session.ctx['user_id']:
        return
    await send_to_superusers(
        f'被群{session.ctx["group_id"]}踢出了。执行者：{session.ctx["operator_id"]}')


# notify superusers when bot is set admin
@on_notice('group_admin.set')
async def _(session: NoticeSession):
    if session.ctx['self_id'] != session.ctx['user_id']:
        return
    await send_to_superusers(
        f'被群{session.ctx["group_id"]}设置为管理员。')


# notify superusers when bot is unset admin
@on_notice('group_admin.unset')
async def _(session: NoticeSession):
    if session.ctx['self_id'] != session.ctx['user_id']:
        return
    await send_to_superusers(
        f'被群{session.ctx["group_id"]}取消管理员。')
