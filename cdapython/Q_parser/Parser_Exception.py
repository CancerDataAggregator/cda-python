from typing import Any, Dict, Tuple


class Error(Exception):
    pass


class ParserError(Error):
    """Any parsing-related error."""


class MissingTokensError(ParserError):
    """When tokens are missing."""


class InvalidTokenError(ParserError):
    """Any error caused by an unexpected token."""


class LexerError(Error):
    """_summary_
    This is made for the Lexing error
    Args:
        Error (_type_): _description_
    """

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> None:
        self.position = kwargs.pop("position", None)
        super().__init__(*args, **kwargs)
