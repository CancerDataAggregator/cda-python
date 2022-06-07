import re
from copy import copy
from typing import TYPE_CHECKING, Optional, Union

from cda_client.model.query import Query
from tdparser import Lexer, Token
from tdparser.topdown import Parser

from cdapython.functions import backwards_comp, col, infer_quote, query_type_conversion

if TYPE_CHECKING:
    from cdapython.Q import Q


def build_query_copy(q: Query) -> Optional[Query]:
    if q is None:
        return None

    Query_value = Query()
    try:
        Query_value.l = build_query_copy(q.l)
    except:
        pass
    try:
        Query_value.r = build_query_copy(q.r)
    except:
        pass

    Query_value.node_type = q.node_type

    try:
        Query_value.value = q.value
    except:
        pass
    return Query_value


class Expression(Token):
    lbp = 0

    def __init__(self, text: str) -> None:
        self.value = str(text).strip()

    def nud(self, context: Parser) -> Query:
        """What the token evaluates to"""
        query = Query()
        query.value = self.value
        return query


class And(Token):
    lbp = 3  # Precedence
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence

        l_copy_query = build_query_copy(left)

        self.query.node_type = "AND"
        self.query.l = l_copy_query

        right_side = context.expression(self.lbp)
        r_copy_query = build_query_copy(right_side)

        self.query.r = r_copy_query
        return self.query


class Or(And):
    lbp = 3  # Precedence
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence

        l_copy_query = build_query_copy(left)

        self.query.node_type = "OR"
        self.query.l = l_copy_query

        right_side = context.expression(self.lbp)
        r_copy_query = build_query_copy(right_side)

        self.query.r = r_copy_query
        return self.query


class Eq(Token):
    lbp = 10  # Precedence
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)

        self.query.node_type = "="
        if isinstance(right_side.value, str) and right_side.value.find("%") != -1:
            returned_node, returned_right = query_type_conversion(
                self.query.node_type, right_side.value
            )
            self.query.node_type = returned_node
            self.query.l = col(backwards_comp(left.value))
            self.query.r = infer_quote(returned_right.value.strip())
            return self.query

        self.query.l = col(backwards_comp(left.value))
        self.query.r = infer_quote(right_side.value)
        return self.query


class NotEq(Token):
    lbp = 5  # Precedence
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "!="
        self.query.l = col(backwards_comp(left.value.strip()))
        self.query.r = infer_quote(right_side.value.strip())
        return self.query


class Greaterthaneq(Token):
    lbp = 5  # Precedence
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = ">="
        self.query.l = col(backwards_comp(left.value.strip()))
        self.query.r = infer_quote(right_side.value.strip())
        return self.query


class Greaterthan(Token):
    lbp = 5  # Precedence
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = ">"
        self.query.l = col(backwards_comp(left.value.strip()))
        self.query.r = infer_quote(right_side.value.strip())
        return self.query


class Lessthaneq(Token):
    lbp = 5  # Precedence
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "<="
        self.query.l = col(backwards_comp(left.value.strip()))
        self.query.r = infer_quote(right_side.value.strip())
        return self.query


class Lessthan(Token):
    lbp = 5  # Precedence
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "<"
        self.query.l = col(backwards_comp(left.value.strip()))
        self.query.r = infer_quote(right_side.value.strip())

        return self.query


class Doublequotes(Token):
    lbp = 10  # Precedence

    def nud(self, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        query.value = self.text

        return query


class ArrayType(Token):

    lbp = 10

    def nud(self, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        query.value = self.text

        return query


class Singlequotes(Doublequotes):
    lbp = 10  # Precedence


class IN(Token):
    lbp = 5
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "IN"
        self.query.l = col(backwards_comp(left.value.strip()))
        self.query.r = infer_quote(right_side.value.strip())
        return self.query


class LIKE(Token):
    lbp = 5
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence

        right_side = context.expression(self.lbp)
        self.query.node_type = "LIKE"
        self.query.node_type, right_side = query_type_conversion(
            self.query.node_type, right_side.value
        )
        self.query.l = col(backwards_comp(left.value.strip()))
        self.query.r = infer_quote(right_side.value.strip())
        return self.query


class NOT(Token):
    lbp = 4
    query = Query()

    def nud(self, context: Parser) -> Query:
        right_side = context.expression(self.lbp)
        self.query.node_type = "NOT"
        self.query.l = right_side
        self.query.r = infer_quote("")
        return self.query


class IS(Token):
    lbp = 19
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence

        right_side = context.expression(self.lbp)

        self.query.node_type = "IS"
        self.query.l = col(backwards_comp(left.value))
        self.query.r = infer_quote(right_side.value)

        return self.query


class IS_NOT(Token):
    lbp = 19
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "IS NOT"
        self.query.l = col(backwards_comp(left.value.strip()))
        self.query.r = infer_quote(right_side.value)
        return self.query


class NOT_IN(Token):
    lbp = 19
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "NOT IN"
        self.query.l = col(backwards_comp(left.value.strip()))
        self.query.r = infer_quote(right_side.value)
        return self.query


class NOT_LIKE:
    lbp = 19
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "NOT LIKE"
        self.query.l = col(backwards_comp(left.value.strip()))
        self.query.r = infer_quote(right_side.value)
        return self.query


class end_token:
    lbp = 0


lexer = Lexer(with_parens=True)
lexer.register_token(
    Expression,
    re.compile(
        r"(\-[\S]+)|(\"[\w\s]+\")|(\b(?!\bAND\b|\band\b)(?!\bOR\b|\bor\b)(?!\bNOT\b|\bnot\b)(?!\bFROM\b|\bfrom\b)(?!\bIN\b|\bin\b)(?!\bLIKE\b|\blike\b)(?!\bIS\b|\bis\b)[\w.\*\+\-_\"\'\=\>\<\{\}\[\]\?\\\:@!#$%\^\&\*\(\)]+\b)"
    ),
)
lexer.register_token(Doublequotes, re.compile(r'(".*?")'))
lexer.register_token(Singlequotes, re.compile(r"('.*?')"))
lexer.register_token(ArrayType, re.compile(r"(\[.*?\])"))
lexer.register_token(Greaterthan, re.compile(r"(\s+>+\s)"))
lexer.register_token(Lessthan, re.compile(r"(\s+<+\s)"))
lexer.register_token(Greaterthaneq, re.compile(r"(\s+>=+\s)"))
lexer.register_token(Lessthan, re.compile(r"(\s+<+\s)"))
lexer.register_token(Lessthaneq, re.compile(r"(\s+<=+\s)"))
lexer.register_token(NotEq, re.compile(r"(\s+!=+\s)"))
lexer.register_token(NotEq, re.compile(r"(\s+<>+\s)"))
lexer.register_token(And, re.compile(r"(AND|and)"))
lexer.register_token(Or, re.compile(r"(OR|or)"))
lexer.register_token(Eq, re.compile(r"(=)"))
lexer.register_token(IN, re.compile(r"(IN|in)"))
lexer.register_token(LIKE, re.compile(r"(LIKE|like)"))
lexer.register_token(NOT, re.compile(r"(NOT|not)"))
lexer.register_token(IS_NOT, re.compile(r"((IS|is)\s+(NOT|not))"))
lexer.register_token(NOT_IN, re.compile(r"((NOT|not)\s+(IN|in))"))
lexer.register_token(NOT_LIKE, re.compile(r"((NOT|not)\s+(LIKE|like))"))
lexer.register_token(IS, re.compile(r"(IS|is)"))


def simple_parser(text: str) -> "Query":
    return lexer.parse(text)
