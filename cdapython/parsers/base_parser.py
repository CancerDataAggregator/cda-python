from ast import arg
from typing import List, Union

from cda_client.model.query import Query
from lark import Token, Tree
from lark.visitors import Transformer


class Base_Parser(Transformer):
    def __init__(self, tree) -> None:
        self.root_node = None

    def _tree_unpacker(self, tree: List[Token]) -> Token:
        """_summary_
        this private method will recursively unpack a value from a tree
        Args:
            tree (List[Token]): _description_

        Returns:
            Token: _description_
        """
        if isinstance(tree, List):
            return self._tree_unpacker(tree[0])
        return tree

    def _walkTree(self, tree: Union[List[Token], List[Tree]]) -> Query:
        pass

    def _str_strip(self, val: str) -> str:
        if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
            return val[1:-1]

        if isinstance(val, str) and val.startswith("'") and val.endswith("'"):
            return val[1:-1]

    def _build_Query(self, args, node_type: str):
        query: Query = Query()
        query.node_type = node_type
        query.l = args[0]
        query.r = args[1]
        return query

    def expression_math(self, args):
        expression_math_query: Query = Query()
        if args[0].node_type == "FUNCTION_NAME":
            expression_math_query.node_type = "FUNCTION_ARG"
            expression_math_query.r = args[0]

        return expression_math_query

    def function(self, args):
        function_query: Query = Query()
        function_query.node_type = "FUNCTION_NAME"
        return function_query

    def number(self, args):
        number_query: Query = Query()
        number_query.node_type = "quoted"
        number_query.value = args[0].value
        return number_query

    def expression_add(self, args):
        expression_query: Query = Query()
        expression_query.node_type = "column"
        expression_query.r = args[0]
        expression_query.l = args[1]
        return expression_query

    def bool_or(self, args):
        return self._build_Query(args, "OR")

    def bool_and(self, args):
        return self._build_Query(args=args, node_type="AND")

    def bool_expression(self, args):
        return args[0]

    def bool_parentheses(self, args):
        return args[0]

    def comparison_type(self, args):
        return args[0]

    def name(self, args):
        return args[0]

    def string(self, args) -> Query:
        string_query: Query = Query()
        string_query.node_type = "quoted"
        string_query.value = self._str_strip(args[0].value)
        return string_query

    def column_name(self, args) -> Query:
        expression_query: Query = Query()
        expression_query.node_type = "column"
        expression_query.value = args[0].value
        return expression_query

    def equals(self, args) -> Query:
        return self._build_Query(args=args, node_type="=")
