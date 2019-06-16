import random as _random

from .typing import Any, Iterable

# fixes aligning problems for multibyte characters
def my_ljust(s, n, fillchar=' ') -> str:
    'same as ljust'
    return s.ljust(n - (len(s.encode("gbk")) - len(s)), fillchar)

def my_rjust(s, n, fillchar=' ') -> str: 
    'same as rjust'
    return s.rjust(n - (len(s.encode("gbk")) - len(s)), fillchar)

def half_none(s: str) -> str:
    'half chance returning s, half chance returning nothing'
    return s if _random.choice((0,1,)) else ''


def prob_pick(itera: Iterable[Any], probs: Iterable[float]) -> Any:
    ''''picks elements randomly from [iter] according to the cumulative
    probability array [probs] which has the same length and ranges from 0 to 1'''
    chosen: float = _random.random()
    if 0 < chosen < probs[0]:
        return itera[0]
    for j in range(len(itera)-1):
        if probs[j] < chosen < probs[j+1]:
            return itera[j+1]
