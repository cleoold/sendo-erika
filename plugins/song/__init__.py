from nonebot import (CommandSession, IntentCommand, MessageSegment, NLPSession,
                     log, on_command, on_natural_language)
from nonebot.permission import *

from utils_bot.command_ops import global_cooldown

from .data_source import get_netease_song_id

__plugin_name__ = '点歌'
__plugin_usage__ = r'''feature: 从网易云分享一首歌曲~

点歌 [歌名]       点一首歌
'''


@on_command('点歌', permission=SUPERUSER | GROUP_MEMBER)
@global_cooldown(1)
async def share_song(session: CommandSession):
    songname: str = session.get('songname')
    songid = await get_netease_song_id(songname)
    report = MessageSegment.music('163', songid) if songid is not None \
        else '未能找到这首歌曲？~'
    await session.send(report)
    log.logger.debug(f'share song called: {report}...')

@share_song.args_parser
async def _(session: CommandSession):
    argStripped: str = session.current_arg_text.strip()

    if session.is_first_run:
        if argStripped:
            session.state['songname'] = argStripped
        else:
            session.finish(__plugin_usage__)

# also match "点歌xxx" without space in between
@on_natural_language(keywords={'点歌'}, permission=SUPERUSER | GROUP_MEMBER)
async def _(session: NLPSession):
    if session.msg_text[:2] == '点歌':
        return IntentCommand(64.0, '点歌', current_arg=session.msg_text[2:])
    return IntentCommand(0, '点歌');
