from ast import arg
from pathlib import Path
from typing import List, Union

from cda_client.model.query import Query
from lark import Lark, Token, Tree, UnexpectedCharacters, UnexpectedToken

from cdapython.exceptions.custom_exception import QSyntaxError
from cdapython.parsers.base_parser import Base_Parser
from cdapython.utils.check_case import check_keyword


class Parse_Q(Base_Parser):
    def __init__(self) -> None:
        self.query = Query()

    def tree(self):
        return self.query

    def q(self, args) -> Query:
        return args[0]

    def like_expr(self, args):
        return self._build_Query(args=args, node_type="LIKE")

    def statement(self, args: Tree):
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

    def equals(self, args: List[Query]) -> Query:
        """_summary_
        This will extract the eq sign
        Args:
            args (_type_): _description_

        Returns:
            Query: _description_
        """
        if "value" in args[1] and "%" in str(args[1].value):
            return self._build_Query(args=args, node_type="LIKE")
        return self._build_Query(args=args, node_type="=")

    def single_quotes(self, args) -> Query:
        quoted_query: Query = Query()
        quoted_query.node_type = "quoted"
        quoted_query.value = args[0].value
        return quoted_query

    def start(self, children):
        return children[0]


def where_parser(text: str):
    sql_grammar = Lark.open(
        "lark/where.lark",
        rel_to=__file__,
        parser="lalr",
        regex=True,
        debug=False,
    )

    try:
        check_keyword(text)
        tree_sql = sql_grammar.parse(text)
        print(tree_sql.pretty())
        return Parse_Q().transform(tree_sql)
    except QSyntaxError as e:
        raise Exception(e)
    except UnexpectedToken as e:
        if e.token.type == "$END":
            raise Exception("Unexpected the End Of Script")
        raise Exception(f"Error in Q statement {e.token.type}")
    except UnexpectedCharacters as e:
        raise Exception(f"Error in Q statement \n {e}")
