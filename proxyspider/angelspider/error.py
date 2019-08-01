
class ResourceDepletionError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理源已用尽 ')




class PoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('The proxy pool is empty')

