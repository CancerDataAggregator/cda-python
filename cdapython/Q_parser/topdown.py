from __future__ import annotations

from typing import TYPE_CHECKING

from .Parser_Exception import MissingTokensError
from .Token import Token

if TYPE_CHECKING:
    from Parser import Parser


class RightParen(Token):
    """_summary_
    A right parenthesis.
    Args:
        Token (_type_): _description_
    """

    def __repr__(self):  # pragma: no cover
        return "<)>"


class LeftParen(Token):
    """_summary_
    A left parenthesis.
    Args:
        Token (_type_): _description_
    """

    token_match = RightParen

    def nud(self, context: Parser):
        # Fetch the next expression
        expr = context.expression()
        # Eat the next token from the flow, and fail if it isn't a right
        # parenthesis.
        context.consume(expect_class=self.token_match)
        return expr

    def __repr__(self):  # pragma: no cover
        return "<(>"


class EndToken(Token):
    """Marks the end of the input."""

    lbp = 0

    def nud(self, context):
        # An 'end' token should never begin an expression.
        raise MissingTokensError("Empty token flow.")

    def led(self, left, context):
        raise MissingTokensError("Unfinished token flow.")

    def __repr__(self):
        return "<End>"
