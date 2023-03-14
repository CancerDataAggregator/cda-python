from __future__ import annotations

from typing import List, Union

from cda_client.model.query import Query
from lark import Lark, Token, Tree
from lark.visitors import Interpreter

from cdapython.parsers.base_parser import Base_Parser


class Parse_Tree(Base_Parser):
    current_node: Query
    output: List[str] = []

    def __init__(self, tree) -> None:
        self.root_node = None
        self.visit(tree)

    def string(self, args) -> Query:
        tmp = Query()
        tmp.node_type = args.data.value
        tmp.l = args.children[0].value
        tmp.r = args.children[1].value
        return tmp

    def _walkTree(self, tree: Union[List[Token], List[Tree]]) -> Query:
        """
        This private method, it will step through the tree to build a query object
        Args:
            tree (Union[List[Token], List[Tree]]): _description_

        Returns:
            Query: _description_
        """
        temp = Query()
        tree_list = None
        if len(tree) != 0:
            tree_list = tree[0]
        if isinstance(tree_list, Tree):
            tree_list = self.visit(tree_list)
        if tree_list and isinstance(tree_list, list):
            for tree_item in tree_list:
                if isinstance(tree_item[0], str):
                    tree_type = tree_item[0].type
                    if tree_type != "FUNCTION_ARG":
                        tree_type = "FUNCTION_ARG"
                    self.output.append(tree_item[0].value)

                elif isinstance(tree_item[0], list):

                    for index, tree_token in enumerate(tree_item):
                        values = self._tree_unpacker(tree=tree_token)
                        if index != len(tree_item):
                            if values is None:
                                self.output.append("'',")
                            else:
                                self.output.append(f"{values.value}")

                    temp.node_type = "FUNCTION_ARG"
                    temp.value = ",".join(self.output)

            temp.r = self._walkTree(tree[1:])

        return temp

    def function(self, args) -> None:
        """
        This will match the lark parse tree key word
        Args:
            args (_type_): _description_
        """
        select_value = Query()
        select_value.node_type = "SELECTVALUES"
        function_node = Query()
        function_name = Query()
        function_node.node_type = str(args.data.value).upper()
        function_node.l = function_name
        function_node.l.node_type = args.children[0].type
        function_node.l.value = args.children[0].value
        function_node.r = self._walkTree(args.children[1:])
        select_value.l = function_node
        if self.root_node is None:
            self.root_node = select_value
            self.current_node = select_value
        else:
            self.current_node.r = select_value
            self.current_node = self.current_node.r

    def tree(self):
        return self.root_node

    def __str__(self) -> str:
        return f"{self.root_node}"


sql_grammar = Lark.open(
    "sql.lark", rel_to=__file__, parser="lalr", regex=True, debug=True
)


def sql_function_parser(text: str) -> Query:
    tree_sql = sql_grammar.parse(text)
    # print(tree_sql.pretty())
    tree = Parse_Tree(tree_sql)
    return tree.tree()
