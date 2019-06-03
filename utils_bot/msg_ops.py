from nonebot import get_bot

bot = get_bot()
SUPERUSERS = bot.config.SUPERUSERS

async def send_to_superusers(msg: str):
    for eachId in SUPERUSERS:
        await bot.send_private_msg(user_id=eachId, message=msg)
