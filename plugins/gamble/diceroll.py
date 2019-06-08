import random

from utils_bot.command_ops import time_limit
from utils_bot.typing import Any

DICE_RESULTS = (
'0',
'''
  . 
 /| 
  | 
  | 
 _|_
''',
'''
 .:::.: 
.:    .:
    .:: 
  .::   
.::     
.:::::::
''',
'''
 ____  
|___ \ 
  __) |
 |__ < 
 ___) |
|____/ 
''',
'''
 _  _   
| || |  
| || |_ 
|__   _|
   | |  
   |_|  
''',
'''
 _____ 
| ____|
| |__  
|___ \ 
 ___) |
|____/ 
''',
'''
        666666
       6::::::
      6::::::6
     6::::::6 
    6::::::6  
   6::::::6   
  6::::::6    
 6::::::::6666
6:::::::::::::
6::::::66666::
6:::::6     6:
6:::::6     6:
6::::::66666::
 66:::::::::::
   66:::::::::
     666666666
''',
)

def roll_dice(pixel:bool=False) -> str:
    '''displays '1'-'6' randomly. if pixel is true then displays image
    '''
    res: int = random.randint(1, 6)
    if pixel:
        return DICE_RESULTS[res].strip()
    else:
        return str(res)

def roll_dice_many(times: Any,
                   errormsg:str='次数太多扔不过来啦~') -> str:
    'weird results come if not int...'
    res: str = ''
    try:
        times = int(times)
        if times > 300000:
            raise TimeoutError
        resDict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
        for _ in range(times):
            r = roll_dice()
            resDict[r] += 1
        for j in ('1', '2', '3', '4', '5', '6'):
            res += f'{j}: {resDict[j]}次\n'
        return res.strip()
    except TimeoutError:
        return errormsg
    # ?
    except ValueError:
        if random.choice((0,0,0,0,1)):
            for j in ('1', '2', '3', '4', '5', '6'):
                res += f'{j}: {hex(random.randint(0x00, 0xFFFFFFFFFFFF))}次\n'
            return res.strip()
        else:
            return '?'
