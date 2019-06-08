import threading as _threading
from contextlib import contextmanager as _contextmanager
from functools import wraps as _wraps

from nonebot import CommandSession as _CommandSession
from nonebot import log as _log

import _thread

from .typing import Awaitable


# decorator
def force_private(f: Awaitable) -> Awaitable:
    '''forces a command to be executed only in private chat
    :args[0]: must be a CommandSession
    '''
    @_wraps(f)
    async def wrapped(*args, **kwargs):
        session: _CommandSession = args[0]
        if session.ctx.get('group_id') or session.ctx.get('discuss_id'):
            _log.logger.debug('forbidden private command terminated.')
            session.finish()
        else:
            return await f(*args, **kwargs)
    return wrapped


# context manager
@_contextmanager
def time_limit(seconds: int, msg:str=''):
    ''' limits the running time of statements inside a with block
    :seconds: stops after [seconds]
    :msg: message to display in logs
    '''
    timer = _threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        _log.logger.debug(f'time out for operation {msg}')
        raise TimeoutError
    finally:
        timer.cancel()
