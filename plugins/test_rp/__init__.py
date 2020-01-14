import random
from datetime import datetime
from pytz import timezone

from nonebot import on_command, CommandSession
from nonebot.permission import *

__plugin_name__ = '今日运气'
__plugin_usage__ = f'''feature: 看看今天的运气~
可用命令：运气
不为结果负责。
'''

class TestLuck:

    @staticmethod
    def return_luck_by_num(num: float) -> str:
        if 0.0 <= num < 0.1:
            return '极坏'
        elif 0.1 <= num < 0.4:
            return '坏'
        elif 0.4 <= num < 0.7:
            return '一般'
        elif 0.7 <= num < 0.9:
            return '好'
        else:
            return '极好'
    
    @classmethod
    def generate_luck_result(cls, sender_id: int) -> str:
        senderId: int = sender_id
        timeStamp: int = int(
            datetime.now().replace(tzinfo=timezone('Asia/Shanghai')).strftime('%m%d%Y')
            )
        seed: int = (senderId * 2) | (timeStamp * 333)
        random.seed(seed)
        res: float = random.random()
        random.seed()
        return cls.return_luck_by_num(res)

@on_command('我的运气', aliases=('运气', '今日运气', '今日人品', '我的人品', 'jrrp', '运势', '今日运势'), permission=GROUP_MEMBER | SUPERUSER)
async def my_luck_today(session: CommandSession):
    senderId: int = int(session.ctx['user_id'])
    await session.send(TestLuck.generate_luck_result(senderId), at_sender=True)
