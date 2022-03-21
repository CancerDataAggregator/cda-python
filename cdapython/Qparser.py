import re
from typing import TYPE_CHECKING, Union

from tdparser import Lexer, Token
from tdparser.topdown import Parser

from cdapython.Q import Q

if TYPE_CHECKING:
    from cdapython.Q import Q


class Expression(Token):
    def __init__(self, text: str) -> None:
        self.value = str(text).strip()

    def nud(self, context: Parser) -> str:
        """What the token evaluates to"""
        return self.value.strip()


class Eq(Token):
    lbp = 10  # Precedence

    def led(self, left: str, context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return Q(left.strip() + " = " + right_side.strip())


class NotEq(Token):
    lbp = 5  # Precedence

    def led(self, left: Union[str, Q], context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        if isinstance(left, Q):
            return left.Not_EQ(right_side)
        else:
            return Q(left.strip() + " != " + right_side.strip())


class Greatertheneq(Token):
    lbp = 4  # Precedence

    def led(self, left: Union[str, Q], context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        if isinstance(left, Q):
            return left.Greater_Then_EQ(right_side)
        else:
            return Q(left.strip() + " >= " + right_side.strip())


class Greaterthen(Token):
    lbp = 4  # Precedence

    def led(self, left: str, context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        if isinstance(left, Q):
            return left.Greater_Then(right_side)
        else:
            return Q(left.strip() + " > " + right_side.strip())


class Lesstheneq(Token):
    lbp = 4  # Precedence

    def led(self, left: str, context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        if isinstance(left, Q):
            return left.Less_Then_EQ(right_side)
        else:
            return Q(left.strip() + " <= " + right_side.strip())


class Lessthen(Token):
    lbp = 4  # Precedence

    def led(self, left: str, context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        if isinstance(left, Q):
            return left.Less_Then(right_side)
        else:
            return Q(left.strip() + " < " + right_side.strip())


class Doublequotes(Token):
    lbp = 10  # Precedence

    def nud(self, context: Parser) -> str:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        value = self
        return value.text


class ArrayType(Token):

    lbp = 10

    def nud(self, context: Parser) -> str:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        value = self
        return value.text


class Singlequotes(Token):
    lbp = 10  # Precedence

    def nud(self, context: Parser) -> str:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        value = self
        return value.text


class And(Token):
    lbp = 3  # Precedence

    def led(self, left: Q, context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return left.And(right_side)


class Or(Token):
    lbp = 6  # Precedence

    def led(self, left: Q, context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return left.Or(right_side)


class From(Token):
    lbp = 2  # Precedence

    def led(self, left: Q, context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return left.From(right_side)


class IN(Token):
    lbp = 4

    def led(self, left: str, context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return Q(left.strip() + " IN " + right_side)


class LIKE(Token):
    lbp = 4

    def led(self, left: str, context: Parser) -> Q:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence

        right_side = context.expression(self.lbp)
        return Q(left.strip() + " LIKE " + right_side)


class var(Token):
    def __init__(self, text: str) -> None:
        self.value = str(text).strip()
        self.symbol_table = {}

    def nud(self, context: Parser) -> str:
        """What the token evaluates to"""
        right_side = context.expression(self.lbp)

        if right_side not in self.symbol_table:
            self.symbol_table[right_side] = right_side

        return self.symbol_table[right_side]


lexer = Lexer(with_parens=True)
lexer.register_token(
    Expression,
    re.compile(
        r"(\-[\S]+)|(\"[\w\s]+\")|(\b(?!\bAND\b)(?!\bOR\b)(?!\bNOT\b)(?!\bFROM\b)(?!\bIN\b)(?!\bLIKE\b)(?!\bVar\b)[\w.\*\+\-_\"\'\=\>\<\{\}\[\]\?\\\:@!#$%\^\&\*\(\)]+\b)"
    ),
)
lexer.register_token(Doublequotes, re.compile(r'(".*?")'))
lexer.register_token(Singlequotes, re.compile(r"('.*?')"))
lexer.register_token(ArrayType, re.compile(r"(\[.*?\])"))
lexer.register_token(Greaterthen, re.compile(r"(\s+>+\s)"))
lexer.register_token(Greatertheneq, re.compile(r"(\s+>=+\s)"))
lexer.register_token(Lessthen, re.compile(r"(\s+<+\s)"))
lexer.register_token(Lesstheneq, re.compile(r"(\s+<=+\s)"))
lexer.register_token(NotEq, re.compile(r"(\s+!=+\s)"))
lexer.register_token(Eq, re.compile(r"(\s+=+\s)"))
lexer.register_token(And, re.compile(r"(AND)"))
lexer.register_token(Or, re.compile(r"(OR)"))
lexer.register_token(From, re.compile(r"(FROM)"))
lexer.register_token(IN, re.compile(r"(IN)"))
lexer.register_token(LIKE, re.compile(r"(LIKE)"))
lexer.register_token(var, re.compile(r"(Var)"))


def parser(text: str) -> Q:
    return lexer.parse(text)
