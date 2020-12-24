from functools import wraps

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@log
def test():
    print("hello world")


test()