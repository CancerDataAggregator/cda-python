from typing import List, NoReturn, Optional, Union

from cda_client.model.query import Query
from lark import Token, Tree
from lark.visitors import Transformer

from cdapython.exceptions.custom_exception import QSyntaxError
from cdapython.parsers.functions import infer_quote, unquoted


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

    def _str_strip(self, val: str) -> Union[str, None]:
        """_summary_
        This is a helper function to strip strings from a node value
        Args:
            val (str): _description_

        Returns:
            Union[str,None]: this will return a string if it exist
        """
        if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
            return val[1:-1]

        if isinstance(val, str) and val.startswith("'") and val.endswith("'"):
            return val[1:-1]

    def _build_Query(self, args, node_type: str):
        """_summary_
        This is a helper function to build Query objs
        Args:
            args (_type_): _description_
            node_type (str): _description_

        Returns:
            _type_: _description_
        """
        query: Query = Query()
        query.node_type = node_type
        query.l = args[0]
        query.r = args[1]
        return query

    def expression_math(self, args):
        expression_math_query: Query = args[0]

        if expression_math_query.node_type == "FUNCTION_NAME":
            args_list = args[1:]
            current_node = expression_math_query
            for i in args_list:
                new_query = Query()
                new_query.node_type = "FUNCTION_ARG"
                new_query.l = i
                current_node.r = new_query
                current_node = new_query
        return expression_math_query

    def count(self, args) -> Query:
        return self.function("count")

    def replace(self, args) -> Query:
        return self.function("replace")

    def function(self, args) -> Query:
        """_summary_
            This will build the a generic function Query obj
        Args:
            args (_type_): _description_

        Returns:
            Query: _description_
        """
        function_query: Query = Query()
        function_query.node_type = "FUNCTION_NAME"
        function_query.value = args
        return function_query

    def neg(self, args) -> Query:
        """_summary_
        This will extract the any negative number
        Args:
            args (_type_): _description_

        Returns:
            Query: _description_
        """
        negative_number_query: Query = Query()
        negative_number_query.node_type = "unquoted"
        negative_number_query.value = f"-{args[0]}"
        return negative_number_query

    def number(self, args: List[Token]):
        """_summary_
        This will extract the any number token in the from the args array
        and create a new Query obj
        Args:
            args (_type_): _description_

        Returns:
            _type_: _description_
        """
        number_query: Query = Query()
        number_query.node_type = "unquoted"
        number_query.value = args[0].value
        return number_query

    def expression_add(self, args):
        """_summary_
        This will extract a addition sign and build a right and left node
        Args:
            args (_type_): _description_

        Returns:
            _type_: _description_
        """

        return self._build_Query(args=args, node_type="+")

    def expression_mul(self, args):
        """_summary_
            This will extract a mulpaction sign and build a right and left node
        Args:
            args (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self._build_Query(args=args, node_type="*")

    def expression_sub(self, args):
        """_summary_
            This will extract a subtraction sign and build a right and left node
        Args:
            args (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self._build_Query(args=args, node_type="-")

    def expression_div(self, args):
        """_summary_
            This will extract a subtraction sign and build a right and left node
        Args:
            args (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self._build_Query(args=args, node_type="/")

    def bool_or(self, args) -> Query:
        """_summary_
        This build a Query Obj
        Args:
            args (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self._build_Query(args, "OR")

    def bool_and(self, args):
        return self._build_Query(args=args, node_type="AND")

    def bool_expression(self, args):
        return args[0]

    def bool_parentheses(self, args):
        return args[0]

    def comparison_type(self, args):
        return args[0]

    def not_op(self, args) -> Query:
        query: Query = Query()
        query.node_type = "NOT"
        query.l = args[0]
        return query

    def not_equals(self, args):
        return self._build_Query(args=args, node_type="!=")

    def greater_than(self, args):
        return self._build_Query(args=args, node_type=">")

    def less_than(self, args):
        return self._build_Query(args=args, node_type="<")

    def greater_than_or_equal(self, args):
        return self._build_Query(args=args, node_type=">=")

    def less_than_or_equal(self, args):
        return self._build_Query(args=args, node_type="<=")

    def is_not_null_op(self, args):
        return self._build_Query(args=args, node_type="IS NOT")

    def is_op(self, args):
        return self._build_Query(args=args, node_type="IS")

    def name(self, args):
        return args[0]

    def null(self, _):
        return unquoted("NULL")

    def array(self, args):
        query = Query()
        query.value = ",".join([i.value for i in args])
        return query

    def in_expr(self, args):
        in_query: Query = Query()
        in_query.node_type = "IN"
        in_query.l = args[0]
        in_query.r = args[1]
        return in_query

    def q_syntax_error_case(self, args) -> NoReturn:
        raise QSyntaxError(keyword=args[0])

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

    def equals(self, args: List[Query]) -> Query:
        """_summary_
        This will extract Query objs from the args array and pass them to the
        build_Query function to build the node
        Args:
            args (_type_): _description_

        Returns:
            Query: _description_
        """
        return self._build_Query(args=args, node_type="=")
