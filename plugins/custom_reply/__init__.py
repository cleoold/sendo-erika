from os import path
import json
import random
import re

from nonebot import CommandSession, on_command, get_bot, log
from nonebot.permission import *

FAILED_MSG = '添加单条消息：add [群号] [模式]\n'\
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
if not path.exists(DATA_PATH):
    with open(DATA_PATH, 'w') as datafile:
        json.dump(
            {"global": {"full_match": {},
                        "inclusive_match": {},
                        "regex_match" : {}} },
        datafile, indent=4)

def load_data() -> dict:
    with open(DATA_PATH) as datafile:
        return json.load(datafile)

# load reply data
REPLIES = load_data()
#groupIds = [k for k in REPLIES.keys() if str.isdecimal(k)] + ['global']

# acquires global event monitor
bot = get_bot()

# auto reply in group chats

def process_var(ctx: Context_T, myText: str) -> str:
    'process whether the reply keyword contains variables.'
    if not re.search(r'{SENDER_.+]', myText):
        return myText
    else:
        # define pointer constants
        try:
            SENDER_ID = str(ctx['sender']['user_id'])
            SENDER_NICK = ctx['sender']['nickname']
            SENDER_CARD = ctx['sender']['card']
            SENDER_ROLE = ctx['sender']['role']
            SENDER_TITLE = ctx['sender']['title']
        except Exception:
            pass
        # when you chose python, you gave up efficiency...
        return myText.replace('{SENDER_ID]', SENDER_ID).\
            replace('{SENDER_NICK]', SENDER_NICK).\
            replace('{SENDER_CARD]', SENDER_CARD).\
            replace('{SENDER_ROLE]', SENDER_ROLE).\
            replace('{SENDER_TITLE]', SENDER_TITLE)

class Get_Out(Exception):
    pass

@bot.on_message('group')
async def handle_keyword_reply(ctx: Context_T):

    currentGroupId = ctx['group_id']
    textReceived = ctx['raw_message']

    # config specific to groups is prioritized
    for groupId in (currentGroupId, 'global'):
        try:
            # handles full_match
            for keyword, reply in REPLIES[str(groupId)]['full_match'].items():
                if textReceived == keyword:
                    toSend = process_var(ctx, random.choice(reply))
                    raise Get_Out
            # handles inclusive_match
            for keyword, reply in REPLIES[str(groupId)]['inclusive_match'].items():
                if keyword in textReceived:
                    toSend = process_var(ctx, random.choice(reply))
                    raise Get_Out
            # handles regex_match
            for keyword, reply in REPLIES[str(groupId)]['regex_match'].items():
                if re.search(keyword, textReceived):
                    toSend = process_var(ctx, random.choice(reply))
                    raise Get_Out
        except Exception:
            pass
    try:
        await bot.send_group_msg(group_id=currentGroupId, message=toSend)
    except NameError:
        pass



# superuser modifies replies
@on_command('群关键字', permission=SUPERUSER)
async def keyword_mod(session: CommandSession):

    try:
        order, groupId, mode = False, False, False
        iniParam = session.get('iniParam')
        order, groupId = iniParam[0], iniParam[1]
        mode = iniParam[2]
    except Exception:
        pass
    log.logger.debug(f'keyword modification called: {order}; {groupId}; {mode}')

    if order == 'add' or order == 'del':
        keyword = session.get('keyword', prompt='在这里输入关键字')
    if order == 'add':
        reply = session.get('reply', prompt='在这里输入回复')
    
    # check args
    if not ((order == 'add' or order == 'del' or order == 'delall')\
        and (groupId.isdecimal() or groupId == 'global')):
        session.finish("指令或群号错误\n" + FAILED_MSG)

    global REPLIES
    from copy import deepcopy
    newReplies = deepcopy(REPLIES)
    if order != 'delall':
        if mode == '1':
            modeStr = 'full_match'
        elif mode == '2':
            modeStr = 'inclusive_match'
        elif mode == '3':
            modeStr = 'regex_match'
        else:
            session.finish("模式错误\n" + FAILED_MSG)

    try:
        if order == 'add':
            newReplies.setdefault(groupId, {})
            newReplies[groupId].setdefault('full_match', {})
            newReplies[groupId].setdefault('inclusive_match', {})
            newReplies[groupId].setdefault('regex_match', {})
            newReplies[groupId][modeStr].setdefault(keyword, [])
            newReplies[groupId][modeStr][keyword].append(reply)
        if order == 'del':
            del newReplies[groupId][modeStr][keyword]
        if order == 'delall':
            if groupId == 'global':
                newReplies['global'] = {"full_match": {},
                                        "inclusive_match": {},
                                        "regex_match" : {} }
            else:
                del newReplies[groupId]
    except KeyError:
        session.finish('当前关键字表不可用或无此关键字')
    
    # make a backup
    try:
        from shutil import copyfile
        copyfile(DATA_PATH, path.join(path.dirname(__file__), 'group_data_bak.json'))
    except Exception as exc:
        session.finish('出现错误。 当前设置没有改动' + str(exc))
    try:
        # replaces previous file
        with open(DATA_PATH, 'w') as datafile:
            json.dump(newReplies, datafile, indent=4, ensure_ascii=False)
    except Exception as exc:
        session.finish(str(exc))
    # load new data
    REPLIES = newReplies
    await session.send('success!')


@keyword_mod.args_parser
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

