#from aiohttp import request
import aiohttp
from nonebot import get_bot

from utils_bot.typing import Union

# code running api source: https://github.com/prasmussen/glot-run/
#         api url and doc: https://glot.io
#         get your token there at https://glot.io/account/token
##
# program attribution: https://github.com/cczu-osa/aki/

RUN_API_URL_FORMAT: str = 'https://glot.io/run/{}?version=latest'

TOKEN: str = get_bot().config.GLOT_RUN_TOKEN

SUPPORTED_LANGS: dict = {
    'assembly': {'ext': 'asm'},
    'bash': {'ext': 'sh'},
    'c': {'ext': 'c'},
    'clojure': {'ext': 'clj'},
    'coffeescript': {'ext': 'coffe'},
    'cpp': {'ext': 'cpp'},
    'csharp': {'ext': 'cs'},
    'erlang': {'ext': 'erl'},
    'fsharp': {'ext': 'fs'},
    'go': {'ext': 'go'},
    'groovy': {'ext': 'groovy'},
    'haskell': {'ext': 'hs'},
    'java': {'ext': 'java', 'name': 'Main'},
    'javascript': {'ext': 'js'},
    'julia': {'ext': 'jl'},
    'kotlin': {'ext': 'kt'},
    'lua': {'ext': 'lua'},
    'perl': {'ext': 'pl'},
    'php': {'ext': 'php'},
    'python': {'ext': 'py'},
    'ruby': {'ext': 'rb'},
    'rust': {'ext': 'rs'},
    'scala': {'ext': 'scala'},
    'swift': {'ext': 'swift'},
    'typescript': {'ext': 'ts'},
}

headers = {'Authorization': f'Token {TOKEN}'}

async def fetch(lang: str, code: str) -> Union[dict, None]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(RUN_API_URL_FORMAT.format(lang),
                headers=headers, raise_for_status=True, timeout=10,
                json={
                    'files': [{
                        'name': (SUPPORTED_LANGS[lang].get('name', 'main') +
                                f'.{SUPPORTED_LANGS[lang]["ext"]}'),
                        "content": code
                    }],
                    'stdin': '',
                    'command': ''}) as req:
                payload: dict = await req.json()
                assert isinstance(payload, dict)
        except Exception:
            return None

    return payload

def process_result(payload: Union[dict, None]) -> str:
    if payload is None:
        return '不可用'
    res: str = ''
    try:
        for k in ('stdout', 'stderr', 'error'):
            val: str = payload.get(k)

            lines: list = val.splitlines()
            lines, linesRemain = lines[:15], lines[15:]
            out, outRemain = val[:80 * 10], val[80 * 10:]

            isCut = '(输出过长，已截断)\n' if linesRemain or outRemain else ''
            Add2End = '' if val or k == 'error' else '\n'
            res += f'{k}: {isCut}{out}{Add2End}'

    except Exception:
        pass
    return res

async def code_run_glot(lang: str, code: str) -> str:
    return process_result(await fetch(lang, code))
