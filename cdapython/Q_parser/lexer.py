import re
from typing import Any, Union

from .Parser import Parser
from .Parser_Exception import LexerError
from .topdown import EndToken, LeftParen, RightParen, Token


class TokenRegistry(object):
    def __init__(self):
        self._tokens: list[tuple[Token, re.Pattern[Any]]] = []

    def register(self, token: Token, regexp: re.Pattern):
        self._tokens.append((token, re.compile(regexp)))

    def matching_tokens(self, text, start=0):
        """Retrieve all token definitions matching the beginning of a text.

        Args:
            text (str): the text to test
            start (int): the position where matches should be searched in the
                string (see re.match(rx, txt, pos))

        Yields:
            (token_class, re.Match): all token class whose regexp matches the
                text, and the related re.Match object.
        """
        for token_class, regexp in self._tokens:
            matchs = regexp.match(text, pos=start)
            if matchs:
                yield token_class, matchs

    def get_token(self, text, start=0):
        best_class: Union[Token, None] = None
        best_match: Union[re.Match[str], None] = None

        for token_class, matchs in self.matching_tokens(text, start=start):
            if best_class and best_match.end() >= matchs.end():
                continue
            best_match = matchs
            best_class = token_class

        return best_class, best_match

    def __len__(self) -> int:
        return len(self._tokens)


class Lexer(object):
    def __init__(
        self,
        with_parens=False,
        blank_chars=(" ", "\t"),
        end_token=EndToken,
        *args,
        **kwargs,
    ):
        self.tokens: TokenRegistry = TokenRegistry()
        self.blank_chars = set(blank_chars)
        self.end_token = end_token

        if with_parens:
            self.register_token(LeftParen, re.compile(r"\("))
            self.register_token(RightParen, re.compile(r"\)"))

        super(Lexer, self).__init__(*args, **kwargs)

    def register_token(self, token_class, regexp=None) -> None:
        """Register a token class.

        Args:
            token_class (tdparser.Token): the token class to register
            regexp (optional str): the regexp for elements of that token.
                Defaults to the `regexp` attribute of the token class.
        """

        if regexp is None:
            regexp = token_class.regexp

        self.tokens.register(token_class, regexp=regexp)

    def register_tokens(self, *token_class) -> None:
        for token_class in token_class:
            self.register_token(token_class=token_class)

    def lex(self, text):
        """Split self.text into a list of tokens.

        Args:
            text (str): text to parse

        Yields:
            Token: the tokens generated from the given text.
        """
        pos = 0
        while text:
            token_class, matchs = self.tokens.get_token(text=text)
            if token_class is not None:
                matched_text = text[matchs.start(): matchs.end()]
                yield token_class(matched_text)
                text = text[matchs.end():]
                pos += matchs.end()
            elif text[0] in self.blank_chars:
                text = text[1:]
                pos += 1
            else:
                raise LexerError(
                    "Invalid character %s in %s" % (text[0], text), position=pos
                )
        yield self.end_token()

    def parse(self, text: str):
        tokens = self.lex(text)
        parser = Parser(tokens)
        return parser.parse()
