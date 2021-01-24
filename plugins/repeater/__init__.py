
import asyncio
import random

from aiocqhttp import Event
from nonebot import get_bot
from nonebot.permission import *

from utils_bot.msg_ops import msg_is_calling_me
from utils_bot.typing import *

__plugin_name__ = '复读机 (private)'
__plugin_usage__ = r'''feature: 复读
人类的本质
'''

# acquires global event monitor
bot = get_bot()

class Record:
    def __init__(self, lastMsg: str, count: int):
        self.lastMsg = lastMsg
        self.count = count

class Records(dict):

    def get_record(self, group_id: str, msg: str) -> Record:
        'creates tracker for each group at beginning'
        record = self.get(group_id)
        if record is None:
            record = Record(msg, 0) # TODO: better semantics
            self[group_id] = record
        return record

    def simple_repeat(self, group_id: str, msg: str,
                            wait_until: int = 3) -> Union[str, None]:
        # creates tracker for each group at beginning
        record = self.get_record(group_id, msg)
        if msg != record.lastMsg:
            record.lastMsg, record.count = msg, 1
            return
        record.count += 1
        if record.count == wait_until:
            record.count = -999
            return msg

    def you_repeat(self, group_id: str, msg: str) -> Union[str, None]:
        'used when message starts with "我"'
        record = self.get_record(group_id, msg)
        if random.choice((0,0,0,0,1)):
            if msg_is_calling_me(msg):
                return
            record.count = -999
            newMsg = []
            for char in msg:
                if char == '我': newMsg.append('你')
                elif char == '你': newMsg.append('我')
                else: newMsg.append(char)
            return ''.join(newMsg)

# key: str
# value: Record
records = Records()

@bot.on_message('group')
async def _(ctx: Event):

    groupId = ctx['group_id']
    msg = ctx['raw_message']

    ## special: if message starts with '我' then reply with the same sentece but with '你'
    if msg.startswith('我'):
        sendMsg = records.you_repeat(groupId, msg)
        # delayed
        if sendMsg is not None:
            await asyncio.sleep(random.randint(1, 10))
    else:
        sendMsg = records.simple_repeat(groupId, msg, 3)
    if sendMsg is not None:
        await bot.send_group_msg(group_id=groupId, message=sendMsg)
