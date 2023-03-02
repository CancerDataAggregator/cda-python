from typing import TYPE_CHECKING, Generator

from .Parser_Exception import InvalidTokenError, MissingTokensError
from .topdown import EndToken

if TYPE_CHECKING:
    from Token import Token


class Parser:
    """Converts lexed tokens into their representation.

    Attributes:
        tokens (iterable of Token): the tokens.
        current_token (Token): the current token
    """

    def __init__(self, tokens: Generator) -> None:
        self.tokens = iter(tokens)
        self.current_pos = 0
        try:
            self.current_token: Token = next(self.tokens)
        except StopIteration:
            raise MissingTokensError("No tokens provided.")

    def _forward(self) -> None:
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            raise MissingTokensError(
                "Unexpected end of token stream at %d." % self.current_pos
            )
        self.current_pos += 1

    def consume(self, expect_class=None):
        """Retrieve the current token, then advance the parser.

        If an expected class is provided, it will assert that the current token
        matches that class (is an instance).

        Note that when calling a token's nud() or led() functions, the "current"
        token is the token following the token whose method has been called.

        Returns:
            Token: the previous current token.

        Raises:
            InvalidTokenError: If an expect_class is provided and the current
                token doesn't match that class.
        """
        if expect_class and not isinstance(self.current_token, expect_class):
            raise InvalidTokenError(
                "Unexpected token at %d: got %r, expected %s"
                % (self.current_pos, self.current_token, expect_class.__name__)
            )
        current_token = self.current_token
        self._forward()
        return current_token

    def expression(self, rbp: int = 0):
        """Extract an expression from the flow of tokens.

        Args:
            rbp (int): the "right binding power" of the previous token.
                This represents the (right) precedence of the previous token,
                and will be compared to the (left) precedence of next tokens.

        Returns:
            Whatever the led/nud functions of tokens returned.
        """
        prev_token = self.consume()

        # Retrieve the value from the previous token situated at the
        # leftmost point in the expression
        left = prev_token.nud(context=self)

        while rbp < self.current_token.lbp:
            # Read incoming tokens with a higher 'left binding power'.
            # Those are tokens that prefer binding to the left of an expression
            # than to the right of an expression.
            prev_token = self.consume()
            left = prev_token.led(left, context=self)

        return left

    def parse(self):
        """Parse the flow of tokens, and return their evaluation."""
        expr = self.expression()
        if not isinstance(self.current_token, EndToken):
            raise InvalidTokenError(
                f"Unconsumed trailing tokens. ERROR With {self.current_token}"
            )
        return expr
