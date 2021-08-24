class MongoEngineDSLError(Exception):
    pass


class InvalidSyntaxError(MongoEngineDSLError):
    pass


class TransformHookError(MongoEngineDSLError):
    def __init__(self, key, exc):
        self.key = key
        self.exc = exc
        self.desc = 'Field %s transform hook error' % key

    def __str__(self):
        return self.desc
