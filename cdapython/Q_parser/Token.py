from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn, TypeVar, Union

from .Parser_Exception import InvalidTokenError

if TYPE_CHECKING:
    from re import Pattern


T = TypeVar("T")


class Token:
    """
    This is the Base class for tokens.

    Ref: tdparser https://github.com/rbarrois/tdparser
    Args:
        object (_type_): _description_
    """

    regexp: Union[str, Pattern] = ""
    """
    Access public variable
    \n
    Used to assign regex to class
    """

    lbp: int = 0
    """
    Access public variable
    \n
    Left binding power
    Controls how much this token binds to a token on its right
    """

    def __init__(self, text: str = "") -> None:
        self.text = text

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.text!r}>"

    def nud(self, context) -> T:
        """Null denotation.

        Describes what happens to this token when located at the beginning of
        an expression.

        Args:
            context (Parser): the parser from which next tokens/subexpressions
                can be retrieved

        Returns:
            object: Parsed value for this token (a node, a value, ...)
        """
        raise InvalidTokenError(
            "Unexpected token %s at the left of an expression (pos: %d)"
            % (self, context.current_pos)
        )

    def led(self, left, context) -> T:
        """Left denotation.

        Describe what happens to this token when appearing inside a construct
        (at the left of the rest of the construct).

        Args:
            context (Parser): the parser from which 'next' data can be
                retrieved
            left (object): the representation of the construct on the
                left of this token

        Returns:
            object built from this token, what is on its right, and
                what was on its left.
        """
        raise InvalidTokenError(
            "Unexpected token %s in the middle of an expression (pos: %d)"
            % (self, context.current_pos)
        )
