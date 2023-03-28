from ast import arg
from pathlib import Path
from typing import List, Union

from cda_client.model.query import Query
from lark import Lark, Token, Tree, UnexpectedToken, v_args

from cdapython.parsers.base_parser import Base_Parser


class Parse_Q(Base_Parser):
    def __init__(self) -> None:
        self.query = Query()

    def tree(self):
        return self.query

    def q(self, args) -> Query:
        return args[0]

    def like_expr(self, args):
        like_query: Query = Query()
        like_query.node_type = "LiKE"
        like_query.r = args[0]
        like_query.l = args[1]
        return like_query

    def statement(self, args: Tree):
        print(args)
        query = args[1]
        query.l = args[0]
        query.r = args[2]
        return query

    def word(self, word: Token):
        return word

    def expression(self, args: Tree) -> Query:
        expression_query: Query = Query()
        expression_query.node_type = "column"
        expression_query.value = args[0].value
        return expression_query

    def from_expr(self, args) -> Query:
        from_query: Query = list(args)[0]
        args_list = args[1:]
        current_node = from_query
        for i in args_list:
            new_query = Query()
            new_query.node_type = "SUBQUERY"
            new_query.l = i
            new_query.r = current_node.r
            current_node.r = new_query
            current_node = new_query
        return from_query

    def eq(self, args) -> Query:
        eq_query = Query()
        eq_query.node_type = "="
        return eq_query

    def single_quotes(self, args) -> Query:
        quoted_query: Query = Query()
        quoted_query.node_type = "quoted"
        quoted_query.value = args[0].value
        return quoted_query

    def start(self, children):
        return children[0]


def where_parser(text: str):
    sql_grammar = Lark.open(
        "lark/where.lark", rel_to=__file__, parser="lalr", regex=True, debug=True
    )

    try:
        tree_sql = sql_grammar.parse(text)
        print(tree_sql.pretty())
        return Parse_Q().transform(tree_sql)
    except UnexpectedToken as e:
        if e.token.type == "$END":
            raise Exception("Unexpected the End Of Script")
        raise Exception(f"Error in Q statement {e.token.type}")
