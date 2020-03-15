from asyncio import gather as _gather
from nonebot import get_bot as _get_bot

bot = _get_bot()
SUPERUSERS = bot.config.SUPERUSERS
MY_NAMES = bot.config.NICKNAME.union({'机器人', '机械人', '复读机'})

async def send_to_superusers(msg: str):
    tasks = [bot.send_private_msg(user_id=eachId, message=msg) for eachId in SUPERUSERS]
    await _gather(*tasks)

def msg_is_calling_me(msg: str) -> bool:
    for myName in MY_NAMES:
        if myName in msg:
            return True
    return False
