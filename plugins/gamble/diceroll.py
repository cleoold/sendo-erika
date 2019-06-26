import random

from utils_bot.typing import Any

__all__ = ['roll_dice_many', 
           'flip_coin_many']

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

def roll_dice_many(times:Any=1) -> str:
    'have to assure [times] is in the form of an int...'
    res: str = ''
    try:
        times = int(times)
        if times == 1:
            return roll_dice(pixel=True)
        
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
        return '次数太多扔不过来啦~'
    except ValueError:
        return '?'


def flip_coin() -> str:
    res: int = random.randint(0, 1)
    return ('反', '正')[res]

def flip_coin_many(times:Any=1) -> str:
    'have to assure [times] is in the form of an int...'
    try:
        times = int(times)
        if times == 1:
            return flip_coin()
        
        if times > 300000:
            raise TimeoutError
        resList = [0, 0]
        for _ in range(times):
            r: int = random.randint(0, 1)
            resList[r] += 1
        return f'正：{resList[1]} 反：{resList[0]}'
    except TimeoutError:
        return '次数太多扔不过来啦~'
    except ValueError:
        return '?'