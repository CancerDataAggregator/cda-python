class Error(Exception):
    pass


class ParserError(Error):
    """Any parsing-related error."""


class MissingTokensError(ParserError):
    """When tokens are missing."""


class InvalidTokenError(ParserError):
    """Any error caused by an unexpected token."""


class LexerError(Error):
    def __init__(self, *args, **kwargs):
        self.position = kwargs.pop("position", None)
        super(LexerError, self).__init__(*args, **kwargs)
