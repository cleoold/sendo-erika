
import random

from nonebot import get_bot
from nonebot.helpers import context_id
from nonebot.permission import *

from utils_bot.typing import *

__plugin_name__ = '复读机 (private)'
__plugin_usage__ = r'''feature: 复读
人类的本质
'''

# acquires global event monitor
bot = get_bot()

class Record:
    def __init__(self, lastMsg: str, count=1):
        self.lastMsg = lastMsg
        self.count = count

class Records(dict):

    def get_record(self, group_id:str, msg:str) -> Record:
        'creates tracker for each group at beginning'
        record = self.get(group_id)
        if record is None:
            record = Record(msg, 1)
            self[group_id] = record
        return record

    async def simple_repeat(self, group_id:str, msg:str,
                            wait_until:int=3):
        # creates tracker for each group at beginning
        record = self.get_record(group_id, msg)
        if msg != record.lastMsg:
            record.lastMsg, record.count = msg, 1
            return
        record.count += 1
        if record.count == wait_until:
            await bot.send_group_msg(group_id=group_id, message=msg)
            record.count = -999
    
    async def you_repeat(self, group_id:str, msg:str):
        'used when message starts with "我"'
        record = self.get_record(group_id, msg)
        if random.choice((0,0,0,0,1)):
            if '你' in msg:
                msg = msg.replace('你', '我')
            await bot.send_group_msg(group_id=group_id, message='你' + msg[1:])
            record.count = -999

records: Dict[str, Record] = Records()

@bot.on_message('group')
async def _(ctx: Context_T):

    groupId = ctx['group_id']
    msg = ctx['raw_message']

    ## special: if message starts with '我' then reply with the same sentece but with '你'
    if msg.startswith('我'):
        await records.you_repeat(groupId, msg)
    ##
    else:
        await records.simple_repeat(groupId, msg)
