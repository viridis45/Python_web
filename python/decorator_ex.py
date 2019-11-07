def hello(func):
    def wrapper():
        print('hihi')
        func()
        print('hihi')
    return wrapper

@hello
def bye():
    print('byebye')

bye()