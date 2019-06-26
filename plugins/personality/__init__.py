import random

from nonebot import CommandSession as CmdS
from nonebot.permission import *

from utils_bot.command_ops import (on_grp_command, on_grp_command_ask,
                                   on_grp_command_do)
from utils_bot.string_ops import half_none, prob_pick

__plugin_usage__ = '一些个性化回复'

@on_grp_command_ask('你是谁', '是谁', '谁')
async def _(s: CmdS): await s.send('sendo erika!')

@on_grp_command_ask('性别', '你的性别')
async def _(s: CmdS): await s.send(f'女{half_none("！")}')

@on_grp_command_ask('年龄', '你的年龄')
async def _(s: CmdS): await s.send(f'16{half_none("！")}')

@on_grp_command_ask('主人是谁', '你的主人是谁', '谁是你的主人')
async def _(s: CmdS): await s.send('没有')

@on_grp_command_ask('你爱我吗', '你爱不爱我', '爱我吗', '爱不爱我')
async def _(s: CmdS): await s.send('想要获得本小姐的青睐，可不是容易的事情噢~')

@on_grp_command_do('结婚', '嫁给我', '我娶你')
async def _(s: CmdS): await s.send('绝对不行')

@on_grp_command('我爱你')
async def _(s: CmdS): await s.send('绝对不行')

                # | | | | ?
                # v v v v
@on_grp_command_do('娇喘', '淫叫', '叫床')
async def _(s: CmdS):
    reply = ('你怎么了？', '哈？', '哈??', '嗯……',
             '……怎么突然说这种话',
             '…哈……哈…唔嗯…………唔哈哈~……啊啊啊',
             '嗯，咯……！啊啊，呀，啊嗯，呷，呼啊，哈……，啊\n——我们，一起！')
    prob = (.1, .35, .6, .75, .9, .96, 1)
    await s.send(prob_pick(reply, prob))
