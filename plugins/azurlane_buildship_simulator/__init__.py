from nonebot import on_command, CommandSession
from nonebot.permission import *
from .simulator import *

__plugin_name__ = '碧蓝航线建造模拟'
__plugin_usage__ = r'''feature: 碧蓝航线建造模拟
可用命令：
轻型舰建造，重型舰建造，特型舰建造
参数:
[次数]次            不超过10次
attribution @ 碧蓝航线wiki
'''

@on_command('碧蓝航线建造模拟', aliases=('碧蓝航线建造'), permission=GROUP_MEMBER | SUPERUSER)
async def build_help(session: CommandSession):
    await session.send(__plugin_usage__)

@on_command('轻型舰建造', permission=GROUP_MEMBER | SUPERUSER)
async def light_build_host(session: CommandSession):
    times = session.get('times')
    await session.send(mass_ship_build_light(times))

@on_command('重型舰建造', permission=GROUP_MEMBER | SUPERUSER)
async def heavy_build_host(session: CommandSession):
    times = session.get('times')
    await session.send(mass_ship_build_heavy(times))

@on_command('特型舰建造', permission=GROUP_MEMBER | SUPERUSER)
async def aircraft_build_host(session: CommandSession):
    times = session.get('times')
    await session.send(mass_ship_build_aircraft(times))

@light_build_host.args_parser
@heavy_build_host.args_parser
@aircraft_build_host.args_parser
async def build_command_arg_parse(session: CommandSession):
    argsStripped = session.current_arg_text.strip(' \n次')

    if argsStripped:
        try:
            times = int(argsStripped)
            assert 0 < times < 11
            session.state['times'] = times
        except ValueError:
            session.finish('?')
        except AssertionError:
            session.finish('次数太多啦~')
    else:
        session.state['times'] = 10 #default
