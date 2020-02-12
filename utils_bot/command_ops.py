import threading as _threading
from contextlib import contextmanager as _contextmanager
from functools import wraps as _wraps
import random as _random

from nonebot import CommandSession as _CommandSession
from nonebot import log as _log
from nonebot import on_command as _on_command
from nonebot.command import CommandHandler_T

import _thread

from .typing import Awaitable, Callable, Generator, Iterable


# decorator
def force_private(f: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
    '''forces a command to be executed only in private chat  
    :wrapped f's args[0]: must be a CommandSession
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
"""
@_contextmanager
def time_limit(seconds: int, msg:str=''):
    ''' limits the running time of statements inside a with block  
    :seconds: stops after [seconds]  
    :msg: message to display in logs  
    what the fak, it terminates the programme
    '''
    timer = _threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        _log.logger.debug(f'time out for operation {msg}')
        raise TimeoutError
    finally:
        timer.cancel()"""

##############################################################################
# these features are subject to low efficiencies, and generate 
# commands that might go beyond control. use at own risks
# they are absolutely NOT RECOMMENDED in your implementations
## command generator
def _names_after_q(names: Iterable[str]) -> Generator[str, None, None]:
    for each in names:
        yield each
        yield f'{each}?'
        yield f'{each}？'

def _names_after_do(names: Iterable[str]) -> Generator[str, None, None]:
    for each in names:
        yield each
        yield f'{each}下'
        yield f'{each}一下'
        yield f'{each}吧'

def _names_after_do2(names: Iterable[str]) -> Generator[str, None, None]:
    for each in names:
        yield each
        yield f'给我{each}'
        yield f'和我{each}'
        yield f'跟我{each}'

# decorators
def on_grp_command_ask(*names: Iterable[str]) -> CommandHandler_T:
    '''default to group chat and superusers.
    automatically generates question marks after command names as aliases
    '''
    namesNew = _names_after_q(names)
    return _on_command(next(namesNew),
                       aliases=(name for name in namesNew),
                       permission=0xF100) # # SUPERUSER | GROUP_MEMBER

def on_grp_command_do(*names: Iterable[str]) -> CommandHandler_T:
    '''default to group chat and superusers.
    automatically generates some pre/suffixes as aliases
    '''
    namesNew = _names_after_do(names)
    namesNew = _names_after_do2(namesNew)
    namesNew = _names_after_q(namesNew)
    return _on_command(next(namesNew),
                       aliases=(name for name in namesNew),
                       permission=0xF100)

def on_grp_command(*names: Iterable[str]) -> CommandHandler_T:
    '''default to group chat and superusers.
    '''
    namesNew = iter(names)
    return _on_command(next(namesNew),
                       aliases=(name for name in namesNew),
                       permission=0xF100)
##############################################################################
