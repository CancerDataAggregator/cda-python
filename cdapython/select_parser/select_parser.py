from __future__ import annotations

from itertools import chain
from typing import List, Optional, Union

from cda_client.model.query import Query
from lark import Lark, Token, Transformer, Tree, Visitor
from lark.visitors import Interpreter


class Parse_Tree(Interpreter):
    current_node: Query

    def __init__(self, tree):
        self.root_node = None
        self.visit(tree)

    def string(self, args) -> Query:
        tmp = Query()
        tmp.node_type = args.data.value
        tmp.l = args.children[0].value
        tmp.r = args.children[1].value
        return tmp

    def _walkTree(self, tree: Union[List[Token], List[Tree]]):
        temp = Query()
        tree_list = None
        if len(tree) != 0:
            tree_list = tree[0]
        if isinstance(tree_list, Tree):
            tree_list = self.visit(tree_list)
        if tree_list and isinstance(tree_list, list):
            for tree_item in tree_list:
                tree_type = tree_item[0].type
                if tree_type != "FUNCTION_ARG":
                    tree_type = "FUNCTION_ARG"

                temp.node_type = tree_type
                temp.value = tree_item[0].value

            temp.r = self._walkTree(tree[1:])
        return temp

    def function(self, args) -> None:
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


sql_grammar = Lark.open("sql.lark", rel_to=__file__, parser="lalr")


def sql_function_parser(text: str):
    tree_sql = sql_grammar.parse(text)
    # print(tree_sql.pretty())
    tree = Parse_Tree(tree_sql)
    return tree.tree()
