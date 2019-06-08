
import random

from nonebot import get_bot
from nonebot.helpers import context_id
from nonebot.permission import *

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

# records = {str: Record}
records = {}

@bot.on_message('group')
async def _(ctx: Context_T):

    groupId = ctx['group_id']
    msg = ctx['raw_message']

    # creates tracker for each group at beginning
    record = records.get(groupId)

    ## special: if message starts with '我' then reply with the same sentece but with '你'
    if msg.startswith('我'):
        if random.choice((0,0,1)):
            await bot.send_group_msg(group_id=groupId, message='你' + msg[1:])
            record.count = -999
            return
    ##

    if record is None:
        record = Record(msg, 1)
        records[groupId] = record
        return

    if msg != record.lastMsg:
        record.lastMsg, record.count = msg, 1
        return

    record.count += 1
    if record.count == 3:
        await bot.send_group_msg(group_id=groupId, message=msg)
        record.count = -999
