import re
from typing import TYPE_CHECKING, Union

from cda_client.model.query import Query
from tdparser import Lexer, Token
from tdparser.topdown import Parser

from cdapython.functions import backwards_comp, col, infer_quote, query_type_conversion

if TYPE_CHECKING:
    from cdapython.Q import Q


class Expression(Token):
    lep = 4

    def __init__(self, text: str) -> None:
        self.value = str(text).strip()

    def led(self, context: Parser) -> str:
        """What the token evaluates to"""
        return self.value.strip()

    def nud(self, context: Parser) -> str:
        """What the token evaluates to"""
        return self.value.strip()


class And(Token):
    # Precedence
    query = Query()

    def led(self, left: str, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "AND"
        self.query.l = infer_quote(left)
        self.query.r = infer_quote(right_side)

        return self.query


class Eq(Token):
    lbp = 10  # Precedence
    query = Query()

    def led(self, left: str, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "="
        self.query.node_type, right_side = query_type_conversion(
            self.query.node_type, right_side
        )

        self.query.l = col(backwards_comp(left))
        self.query.r = infer_quote(right_side)

        return self.query


class NotEq(Token):
    lbp = 5  # Precedence
    query = Query()

    def led(self, left: Union[str, Query], context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "!="
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side.strip())
        return self.query


class Greaterthaneq(Token):
    lbp = 4  # Precedence
    query = Query()

    def led(self, left: Union[str, Query], context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = ">="
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side.strip())
        return self.query


class Greaterthan(Token):
    lbp = 4  # Precedence
    query = Query()

    def led(self, left: Union[str, Query], context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = ">"
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side.strip())
        return self.query


class Lessthaneq(Token):
    lbp = 4  # Precedence
    query = Query()

    def led(self, left: Union[str, Query], context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "<="
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side.strip())
        return self.query


class Lessthan(Token):
    lbp = 4  # Precedence
    query = Query()

    def led(self, left: Union[str, Query], context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "<"
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side.strip())

        return self.query


class Doublequotes(Token):
    lbp = 10  # Precedence

    def nud(self, context: Parser) -> str:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        value = self
        return str(value.text)


class ArrayType(Token):

    lbp = 10

    def nud(self, context: Parser) -> str:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        value = self
        return str(value.text)


class Singlequotes(Token):
    lbp = 10  # Precedence

    def nud(self, context: Parser) -> str:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        value = self
        return str(value.text)


class IN(Token):
    lbp = 4
    query = Query()

    def led(self, left: str, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "IN"
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side.strip())
        return self.query

    # def nud(self, context: Parser) -> Query:
    #     right_side = context.expression(self.lbp)
    #     print(context.current_token)
    #     print(type(right_side))
    #     self.query.node_type = "IN"
    #     self.query.l = infer_quote("")
    #     self.query.r = infer_quote(right_side.strip())
    #     return self.query


class LIKE(Token):
    lbp = 4
    query = Query()

    def led(self, left: str, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence

        right_side = context.expression(self.lbp).strip()
        self.query.node_type = "LIKE"
        self.query.node_type, right_side = query_type_conversion(
            self.query.node_type, right_side
        )
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side)
        return self.query


class NOT(Token):
    lbp = 18
    query = Query()

    def nud(self, context: Parser) -> Query:
        right_side = context.expression(self.lbp)
        self.query.node_type = "NOT"
        self.query.l = infer_quote(right_side)
        self.query.r = infer_quote("")
        return self.query


class IS(Token):
    lbp = 19
    query = Query()

    def led(self, left: Union[str, Query], context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        print(context.current_token)
        right_side = context.expression(self.lbp)
        print(context.current_token)
        self.query.node_type = "IS"
        print(type(right_side), type(left))
        if isinstance(left, Query):
            self.query.l = left
        else:
            self.query.l = col(backwards_comp(left))
            self.query.r = infer_quote(right_side)
        return self.query


class IS_NOT(Token):
    lbp = 19
    query = Query()

    def led(self, left: str, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "IS NOT"
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side)
        return self.query


class NOT_IN(Token):
    lbp = 19
    query = Query()

    def led(self, left: str, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "NOT IN"
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side)
        return self.query


class NOT_LIKE:
    lbp = 19
    query = Query()

    def led(self, left: str, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        self.query.node_type = "NOT LIKE"
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side)
        return self.query


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
lexer.register_token(Eq, re.compile(r"(=)"))
lexer.register_token(IN, re.compile(r"(IN|in)"))
lexer.register_token(LIKE, re.compile(r"(LIKE|like)"))
lexer.register_token(NOT, re.compile(r"(NOT|not)"))
lexer.register_token(IS_NOT, re.compile(r"((IS|is)\s+(NOT|not))"))
lexer.register_token(NOT_IN, re.compile(r"((NOT|not)\s+(IN|in))"))
lexer.register_token(NOT_IN, re.compile(r"((NOT|not)\s+(LIKE|like))"))
lexer.register_token(IS, re.compile(r"(IS|is)"))


def simple_parser(text: str) -> "Query":
    return lexer.parse(text)
