from functools import wraps

def log(func):
    @wraps(func)
    def wrapper():
        return func()

    return wrapper


@log
def test():
    print("hello world")


test()
