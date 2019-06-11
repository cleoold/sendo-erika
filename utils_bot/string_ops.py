
# fixes aligning problems for multibyte characters
def my_ljust(s, n): 
    return s.ljust(n - (len(s.encode("gbk")) - len(s)))

def my_rjust(s, n): 
    return s.rjust(n - (len(s.encode("gbk")) - len(s)))