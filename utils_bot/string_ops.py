import random

# fixes aligning problems for multibyte characters
def my_ljust(s, n, fillchar=' ') -> str:
    'same as ljust'
    return s.ljust(n - (len(s.encode("gbk")) - len(s)), fillchar)

def my_rjust(s, n, fillchar=' ') -> str: 
    'same as rjust'
    return s.rjust(n - (len(s.encode("gbk")) - len(s)), fillchar)

def half_none(s: str) -> str:
    'half chance returning s, half chance returning nothing'
    return s if random.choice((0,1,)) else ''