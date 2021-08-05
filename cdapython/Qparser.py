from cdapython.Q import Q
import re
from tdparser import Lexer, Token


class Expression(Token):
    def __init__(self, text: str):
        self.value = str(text).strip()

    def nud(self, context):
        """What the token evaluates to"""
        return self.value.strip()


class Eq(Token):
    lbp = 10  # Precedence

    def led(self, left: str, context):
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return Q(left.strip()+" = "+right_side.strip())


class Greaterthen(Token):
    lbp = 10  # Precedence

    def led(self, left: str, context):
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return Q(left.strip()+" > "+right_side.strip())


class Lessthen(Token):
    lbp = 10  # Precedence

    def led(self, left: str, context):
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return Q(left.strip()+" < "+right_side.strip())
class Doublequotes(Token):
    lbp = 10  # Precedence
    

    def nud(self, context):
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        value = self
        return value.text


class And(Token):
    lbp = 5 # Precedence

    def led(self, left: Q, context):
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return left.And(right_side)


class Or(Token):
    lbp = 6  # Precedence

    def led(self, left: Q, context):
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return left.Or(right_side)


lexer = Lexer(with_parens=True)
lexer.register_token(Expression, re.compile(r'(\-[\S]+)|(\"[\w\s]+\")|(\b(?!\bAND\b)(?!\bOR\b)(?!\bNOT\b)[\w.\*\+\-_\"\'\=\>\<\{\}\[\]\?\\\:@!#$%\^\&\*\(\)]+\b)'))
lexer.register_token(Doublequotes, re.compile(r'(".*?")'))
lexer.register_token(Greaterthen, re.compile(r'(\s+>+\s)'))
lexer.register_token(Lessthen, re.compile(r'(\s+<+\s)'))
lexer.register_token(Eq, re.compile(r'(\s+=+\s)'))
lexer.register_token(And, re.compile(r'(AND)'))
lexer.register_token(Or, re.compile(r'(OR)'))


def parser(text):
    return lexer.parse(text)
