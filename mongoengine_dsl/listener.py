from functools import partialmethod, wraps

from mongoengine import Q
from mongoengine_dsl.errors import InvalidSyntaxError, TransformHookError
from mongoengine_dsl.lexer.MongoEngineDSLListener import MongoEngineDSLListener
from mongoengine_dsl.lexer.MongoEngineDSLParser import MongoEngineDSLParser
from mongoengine_dsl.utils import smart_bool


class Antlr4Listener(MongoEngineDSLListener):
    def __init__(self, transform=None, debug_mode=False):
        self.transform_hooks = transform or {}
        self.debug_mode = debug_mode

        # array
        self.arr_depth = 0
        self.arr_queue = {}

        # Build stages
        self.filter_queue = []  # stage 1
        self.polish_notation = []  # stage 2
        self.query = None  # stage 3

    def __getattribute__(self, name):  # pragma: no cover
        attr = object.__getattribute__(self, name)
        if (
            hasattr(attr, '__call__')
            and name not in ['enterEveryRule', 'exitEveryRule']
            and self.debug_mode
        ):

            @wraps(attr)
            def new_func(*args, **kwargs):
                print('- %s()' % name)
                result = attr(*args, **kwargs)
                print('arr:', self.arr_depth, self.arr_queue)
                print('queue:', self.filter_queue)
                print('notation:', self.polish_notation)
                return result

            return new_func
        else:
            return attr

    # Filter
    def generic_process(self, to=None, ctx=None):
        if to is None:  # pragma: no cover
            raise NotImplementedError('Generic "to" param missing')
        if ctx is None:  # pragma: no cover
            raise NotImplementedError('Generic "ctx" param missing')
        val = to(ctx.getText())

        if self.arr_depth > 0:
            self.arr_queue[self.arr_depth].append(val)
        else:
            self.filter_queue.append(val)

    exitField = partialmethod(generic_process, str)
    exitOperator = partialmethod(generic_process, str)
    exitBooleanValue = partialmethod(generic_process, smart_bool)
    exitQuoteStringValue = partialmethod(
        generic_process, lambda x: x[1:-1].replace('\\"', '"').replace("\\'", "'")
    )
    exitIntegerValue = partialmethod(generic_process, int)
    exitDoubleValue = partialmethod(generic_process, float)
    exitTokenValue = partialmethod(generic_process, str)

    def exitWildcardValue(self, ctx: MongoEngineDSLParser.WildcardValueContext):
        if self.arr_depth > 0:
            raise InvalidSyntaxError('Wildcard operator cannot be used in arrays')
        if self.filter_queue.pop() not in [':', '=', '==']:
            raise InvalidSyntaxError('Wildcard operator can only be used for equals')
        self.filter_queue.extend([':*', True])

    def exitDeniedValue(self, ctx: MongoEngineDSLParser.DeniedValueContext):
        if self.arr_depth > 0:
            raise InvalidSyntaxError('Exclude operator cannot be used in arrays')
        if self.filter_queue.pop() not in [':', '=', '==']:
            raise InvalidSyntaxError('Exclude operator can only be used for equals')
        self.filter_queue.extend([':!', False])

    def exitFilterExpression(self, ctx: MongoEngineDSLParser.FilterExpressionContext):
        if len(self.filter_queue) != 3:  # pragma: no cover
            raise NotImplementedError('Lexer invalid filter size')

        field, op, value = self.filter_queue

        # Operator convert
        mapping = {
            ':': '',
            '=': '',
            '==': '',
            '!=': '__ne',
            '>': '__gt',
            '>=': '__gte',
            '<': '__lt',
            '<=': '__lte',
            ':*': '__exists',
            ':!': '__exists',
            '@': '__in',
            '!@': '__nin',
        }

        no_transform_op = [':*', ':!']

        # value transform
        if (
            field in self.transform_hooks
            and callable(self.transform_hooks[field])
            and op not in no_transform_op
        ):
            try:
                value = self.transform_hooks[field](value)
            except Exception as e:
                raise TransformHookError(key=field, exc=e)

        # operator mapping
        if op not in mapping:  # pragma: no cover
            raise NotImplementedError('Operator %s not support' % op)
        op = mapping[op]

        # field sep
        field = field.replace('.', '__')

        # filter exit
        self.polish_notation.append(Q(**{field + op: value}))
        self.filter_queue.clear()

    # Filter end

    # Logical
    def exitAndExpression(self, ctx: MongoEngineDSLParser.AndExpressionContext):
        self.polish_notation.append('and')

    def exitOrExpression(self, ctx: MongoEngineDSLParser.OrExpressionContext):
        self.polish_notation.append('or')

    # Logical end

    # Array
    def enterArrayValue(self, ctx: MongoEngineDSLParser.ArrayValueContext):
        self.arr_depth += 1
        self.arr_queue[self.arr_depth] = []

    def exitArrayValue(self, ctx: MongoEngineDSLParser.ArrayValueContext):
        self.arr_queue.setdefault(self.arr_depth - 1, [])
        self.arr_queue[self.arr_depth - 1].append(self.arr_queue.get(self.arr_depth))
        self.arr_queue.pop(self.arr_depth)
        self.arr_depth -= 1

        if self.arr_depth == 0:
            self.filter_queue.append(self.arr_queue.pop(0).pop(0))

    # Array end

    def exitProcess(self, ctx: MongoEngineDSLParser.ProcessContext):
        stack = []
        for item in self.polish_notation:
            if item in ['and', 'or']:
                right = stack.pop()
                left = stack.pop()
                if item == 'and':
                    stack.append(left & right)
                elif item == 'or':
                    stack.append(left | right)
                else:  # pragma: no cover
                    raise NotImplementedError('Lexer invalid operator')

            else:
                stack.append(item)

        if len(stack) != 1:  # pragma: no cover
            raise InvalidSyntaxError('Statement is not closed')

        self.query = stack[0]
