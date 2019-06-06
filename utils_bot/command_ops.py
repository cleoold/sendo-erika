from functools import wraps as _wraps
from typing import Awaitable as _Awaitable

from nonebot import CommandSession as _CommandSession
from nonebot import log as _log


def force_private(f: _Awaitable) -> _Awaitable:
    '''forces a command to be executed only in private chat
    :args[0]: must be a CommandSession
    '''
    @_wraps(f)
    async def wrapped(*args, **kwargs):
        session: _CommandSession = args[0]
        if 'group_id' in session.ctx.keys():
            _log.logger.debug('forbidden private command terminated.')
            session.finish()
        return await f(*args, **kwargs)
    return wrapped
