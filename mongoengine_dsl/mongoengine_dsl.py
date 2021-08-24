from typing import Callable, Dict, Union

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from mongoengine import Q
from mongoengine.queryset.visitor import QCombination
from mongoengine_dsl.lexer.MongoEngineDSLLexer import MongoEngineDSLLexer
from mongoengine_dsl.lexer.MongoEngineDSLParser import MongoEngineDSLParser
from mongoengine_dsl.listener import Antlr4Listener


def build_q(
    query: str, listener_clazz=Antlr4Listener, **listener_kwargs
) -> Union[Q, QCombination]:
    """
    Build mongoengine.Q object from DSL query string

    Args:
        query: The query string
        listener_clazz: Antlr4 walker listener
        **listener_kwargs: Antlr4 walker listener params

    Returns:
        Q object for mongoengine queryset filter
    """
    in_stream = InputStream(query)

    lexer = MongoEngineDSLLexer(in_stream)
    stream = CommonTokenStream(lexer)
    parser = MongoEngineDSLParser(stream)
    tree = parser.process()

    listener = listener_clazz(**listener_kwargs)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    return listener.query


class Query:
    def __new__(
        cls, query: str, transform: Dict[str, Callable] = None
    ) -> Union[Q, QCombination]:
        """
        Proxy to build_q()

        Args:
            query: The query string
            transform: key-callable pairs for field data transform, call at build time

        Returns:
            Same as build_q()
        """
        return build_q(query=query, transform=transform)
