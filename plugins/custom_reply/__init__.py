import json
import random
import re
from os import path

import asyncio

from aiocqhttp import Event
from nonebot import CommandSession, get_bot, log, on_command
from nonebot.permission import *

from utils_bot.command_ops import force_private

FAILED_MSG = '查看关键字对：view [群号] [模式]\n'\
            '添加单条消息：add [群号] [模式]\n'\
            '删除单条消息：del [群号] [模式]\n'\
            '删除指定群：delall [群号]\n'\
            '模式：完全匹配-1，包含匹配-2，正则匹配-3'

__plugin_name__ = '自定义群聊回复 (private)'
__plugin_usage__ = r'''feature: 自定义回复

从 json 文件读取自定义回复并且响应群聊。
可以私聊机器人添加或删除机器人，其改变即时生效
''' + FAILED_MSG

# define reply data file path
DATA_PATH = path.join(path.dirname(__file__), 'group_data.json')

DEFAULT_GROUP_DICT: dict = {
    "full_match": {},
    "inclusive_match": {},
    "regex_match" : {}
}

def load_data() -> dict:
    if not path.exists(DATA_PATH):
        with open(DATA_PATH, 'w') as datafile:
            json.dump({
                "global": DEFAULT_GROUP_DICT
            }, datafile, indent=4)
    with open(DATA_PATH) as datafile:
        return json.load(datafile)

# load reply data
REPLIES: dict = load_data()

# acquires global event monitor
bot = get_bot()

# auto reply in group chats

def process_var(ctx: Event, myText: str) -> str:
    'process whether the reply keyword contains variables.'
    if not re.search(r'{SENDER_.+]', myText):
        return myText
    # define pointer constants
    SENDER_ID: str = str(ctx['sender']['user_id'])
    SENDER_NICK: str = ctx['sender']['nickname']
    SENDER_CARD: str = ctx['sender']['card']
    SENDER_ROLE: str = ctx['sender']['role']
    SENDER_TITLE: str = ctx['sender']['title']
    # when you chose python, you gave up efficiency...
    return myText.replace('{SENDER_ID]', SENDER_ID).\
        replace('{SENDER_NICK]', SENDER_NICK).\
        replace('{SENDER_CARD]', SENDER_CARD).\
        replace('{SENDER_ROLE]', SENDER_ROLE).\
        replace('{SENDER_TITLE]', SENDER_TITLE)

class _Get_Out(Exception):
    pass

@bot.on_message('group')
async def handle_keyword_reply(ctx: Event):

    currentGroupId: int = ctx['group_id']
    textReceived: str = ctx['raw_message']

    # config specific to groups is prioritized
    for groupId in (str(currentGroupId), 'global'):
        try:
            # handles full_match
            mayReply = REPLIES[groupId]['full_match'].get(textReceived, None)
            if mayReply is not None:
                toSend: str = process_var(ctx, random.choice(mayReply))
                raise _Get_Out
            # handles inclusive_match
            for keyword, reply in REPLIES[groupId]['inclusive_match'].items():
                if keyword in textReceived:
                    toSend: str = process_var(ctx, random.choice(reply))
                    raise _Get_Out
            # handles regex_match
            for keyword, reply in REPLIES[groupId]['regex_match'].items():
                if re.search(keyword, textReceived):
                    toSend: str = process_var(ctx, random.choice(reply))
                    raise _Get_Out
        except KeyError:
            # REPLIES[str(groupId)] may not exist, go to global
            pass
        except _Get_Out:
            break
    try:
        toSend
        # waits few secs before sending message
        await asyncio.sleep(random.randint(1,5))
        await bot.send_group_msg(group_id=currentGroupId, message=toSend)
    except NameError:
        pass



# superuser can modify replies

class keyword_ops:
    'operations on keyword dict'
    def __init__(self, repliesDict,
                    order='', groupId='', mode='', keyword='', reply=''):
        """
        :param order: 'add', 'del', 'delall' or 'view'
        :param groupId: digits or 'global'
        :param mode: '1', '2' or '3'
        :param keyword: keyword
        :param reply: reply
        """
        if order not in ('add', 'del', 'delall', 'view'):
            raise Exception("指令错误\n" + FAILED_MSG)
        if not groupId.isdecimal() and groupId != 'global':
            raise Exception("群号错误\n" + FAILED_MSG)
        if order != 'delall':
            if mode == '1':
                self.modeStr: str = 'full_match'
            elif mode == '2':
                self.modeStr: str = 'inclusive_match'
            elif mode == '3':
                self.modeStr: str = 'regex_match'
            else:
                raise Exception("模式错误\n" + FAILED_MSG)

        from copy import deepcopy
        self.repliesDict: dict = deepcopy(repliesDict)
        self.order: str = order
        self.groupId: str = groupId
        self.mode: str = mode
        self.keyword: str = keyword
        self.reply: str = reply

    def add(self):
        self.repliesDict.setdefault(self.groupId, DEFAULT_GROUP_DICT)
        modifyPlace = self.repliesDict[self.groupId][self.modeStr]
        modifyPlace.setdefault(self.keyword, [])
        modifyPlace[self.keyword].append(self.reply)

    def dele(self):
        del self.repliesDict[self.groupId][self.modeStr][self.keyword]

    def delall(self):
        if self.groupId == 'global':
            self.repliesDict['global'] = DEFAULT_GROUP_DICT
        else:
            del self.repliesDict[self.groupId]

    @staticmethod
    def backup():
        from shutil import copyfile
        copyfile(DATA_PATH, path.join(path.dirname(__file__), 'group_data_bak.json'))

    def rewrite(self):
        with open(DATA_PATH, 'w') as datafile:
            json.dump(self.repliesDict, datafile, indent=4, ensure_ascii=False)
    
    def send(self):
        return self.repliesDict

    def view_keywords(self) -> str:
        'NOTHROW. returns the keyword pairs for group --> mode'
        try:
            pos: dict = self.repliesDict[self.groupId][self.modeStr]
            res: str = f'{self.groupId}, {self.modeStr}\n'
            for k, v in pos.items():
                if len(v) > 10:
                    v = v[:10] + ['...']
                res += '"{}": "{}"\n'.format(k, '"; "'.join(v))
            if pos == {}:
                res += '(空)'
            res = res.rstrip('\n')
        except KeyError:
            res = '群号错误？'
        return res

    def modify_keywords(self) -> dict:
        'modifies the keyword json file, returns the new keyword dict'
        try:
            if self.order == 'add':
                self.add()
            elif self.order == 'del':
                self.dele()
            elif self.order == 'delall':
                self.delall()
        except KeyError:
            raise Exception('当前关键字表不可用或无此关键字')

        try:
            self.backup()
        except Exception as exc:
            raise Exception('出现错误。 当前设置没有改动' + str(exc))
        self.rewrite()

        return self.send()


# keyword interface
@on_command('群关键字', permission=SUPERUSER)
@force_private
async def keyword_mod(session: CommandSession):

    order, groupId, mode = '', '', ''
    iniParam: list = session.get('iniParam')
    try:
        order = iniParam[0]
        groupId = iniParam[1]
        mode = iniParam[2]
    except Exception:
        pass
    log.logger.debug(f'keyword modification called: {order}; {groupId}; {mode}')
    ##################################################################

    global REPLIES
    # get keyword mod object
    try:
        keymod = keyword_ops(REPLIES, order, groupId, mode)
    except Exception as exc:
        session.finish(str(exc))
    # VIEW order
    if order == 'view':
        session.finish(keymod.view_keywords())
    # MODIFY order
    if order in ['add', 'del']:
        keymod.keyword = session.get('keyword', prompt='在这里输入关键字')
    if order == 'add':
        keymod.reply = session.get('reply', prompt='在这里输入回复')
    try:
        REPLIES = keymod.modify_keywords()
        session.finish('success!')
    except Exception as exc:
        session.finish(str(exc))


@keyword_mod.args_parser
@force_private
async def keyword_mod_arg(session: CommandSession):
    argStripped = session.current_arg_text.strip()

    if session.is_first_run:
        if argStripped:
            session.state['iniParam'] = argStripped.split(' ')
        # if no arg given at first
        else:
            session.finish(FAILED_MSG)
    elif session.current_key == 'keyword':
        session.state['keyword'] = argStripped
    elif session.current_key == 'reply':
        session.state['reply'] = argStripped
