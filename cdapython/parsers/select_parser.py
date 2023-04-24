from __future__ import annotations

from typing import List, Union

from cda_client.model.query import Query
from lark import Lark, Token, Tree
from lark.visitors import Interpreter

from cdapython.parsers.base_parser import Base_Parser


class Parse_Tree(Base_Parser):
    def __init__(self) -> None:
        self.query = Query()

    def select_expression(self, args):
        select_values_query: Query = Query()
        select_values_query.node_type = "SELECTVALUES"
        select_values_query.value = args[0].value
        return select_values_query

    def select(self, args: List[Query]):
        select_query: Query = list(args)[0]
        if select_query.node_type == "SELECTVALUES":
            select_query.value = ",".join([i.value for i in args])
        return select_query

    def set_expr(self, args):
        return args[0]

    def final(self, args):
        return args[0]


sql_grammar = Lark.open(
    "sql_select.lark", rel_to=__file__, parser="lalr", regex=True, debug=True
)


def sql_function_parser(text: str) -> Query:
    tree_sql = sql_grammar.parse(text)
    # print(tree_sql.pretty())
    return Parse_Tree().transform(tree_sql)
