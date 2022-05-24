import re
from typing import TYPE_CHECKING, Union

from tdparser import Lexer, Token
from tdparser.topdown import Parser
from cda_client.model.query import Query


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

        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side.strip())

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


class LIKE(Token):
    lbp = 4
    query = Query()

    def led(self, left: str, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence

        right_side = context.expression(self.lbp)
        self.query.node_type = "LIKE"
        self.query.l = col(backwards_comp(left.strip()))
        self.query.r = infer_quote(right_side.strip())
        return self.query


class NOT(Token):
    lbp = 20
    query = Query()

    def nud(self, context: Parser) -> Query:
        right_side = context.expression(self.lbp)
        self.query.node_type = "NOT"
        self.query.l = None
        self.query.r = infer_quote(right_side.strip())
        return self.query

    def led(self, left: str, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence

        right_side = context.expression(self.lbp)
        self.query.node_type = "NOT"
        self.query.l = None
        self.query.r = infer_quote(right_side.strip())
        return self.query


class IS(Token):
    lbp = 20
    query = Query()

    def nud(self, context: Parser) -> Query:
        right_side = context.expression(self.lbp)
        self.query.node_type = "IS"
        self.query.l = None
        self.query.r = infer_quote(right_side.strip())
        return self.query

    def led(self, left: str, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence

        right_side = context.expression(self.lbp)
        self.query.node_type = "IS"
        self.query.l = None
        self.query.r = infer_quote(right_side.strip())
        return self.query


lexer = Lexer(with_parens=True)
lexer.register_token(
    Expression,
    re.compile(
        r"(\-[\S]+)|(\"[\w\s]+\")|(\b(?!\bAND\b)(?!\bOR\b)(?!\bNOT\b)(?!\bFROM\b)(?!\bIN\b)(?!\bLIKE\b)(?!\bIS\b)[\w.\*\+\-_\"\'\=\>\<\{\}\[\]\?\\\:@!#$%\^\&\*\(\)]+\b)"
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
lexer.register_token(Eq, re.compile(r"(=)"))
lexer.register_token(IN, re.compile(r"(IN)"))
lexer.register_token(LIKE, re.compile(r"(LIKE)"))
lexer.register_token(NOT, re.compile(r"(NOT)"))
lexer.register_token(IS, re.compile(r"(IS)"))


def simple_parser(text: str) -> "Query":
    return lexer.parse(text)
