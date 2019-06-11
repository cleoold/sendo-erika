
# fixes aligning problems for multibyte characters
def my_ljust(s, n, fillchar=' '): 
    return s.ljust(n - (len(s.encode("gbk")) - len(s)), fillchar)

def my_rjust(s, n, fillchar=' '): 
    return s.rjust(n - (len(s.encode("gbk")) - len(s)), fillchar)