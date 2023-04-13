import re
from typing import Any, Optional, Tuple, Union

from cda_client.model.query import Query
from typing_extensions import Literal

from cdapython.parsers.functions import col, infer_quote, query_type_conversion
from cdapython.parsers.Q_parser import Lexer, Token
from cdapython.parsers.Q_parser.Parser import Parser
from cdapython.utils.check_case import check_keyword


def build_query_copy(q: Query) -> Optional[Query]:
    """
    This is for passing by ref instead of value this is a fix for python's copy error
    Args:
        q (Query): _description_

    Returns:
        Optional[Query]: _description_
    """
    if q is None:
        return None

    query_value = Query()
    try:
        query_value.l = build_query_copy(q.l)
    except Exception:
        pass
    try:
        query_value.r = build_query_copy(q.r)
    except Exception:
        pass

    query_value.node_type = q.node_type

    try:
        query_value.value = q.value
    except Exception:
        pass
    return query_value


def like_converter(query: Query, right_side: Query, left: Query) -> Query:
    """_summary_
    This is used to auto covert into a LIKE operator
    Args:
        query (Query): _description_
        right_side (Query): _description_
        left (Query): _description_

    Returns:
        Query: _description_
    """
    returned_node: str
    returned_right: Query

    returned_node, returned_right = query_type_conversion(
        query.node_type, right_side.value
    )

    query.node_type = returned_node
    query.l = col(left.value)
    query.r = infer_quote(returned_right.value.strip())
    return query


def is_float(num) -> bool:
    """_summary_
    This is a helper function used to check if a number is a float
    Args:
        num (_type_): _description_

    Returns:
        bool: _description_
    """
    float_regex: re.Pattern[str] = re.compile(r"[-+]?\d*\.\d+")
    if re.match(float_regex, num) is not None:
        return True
    else:
        return False


class Decimal_Number(Token):
    """_summary_
        This Token is used to evaluate Decimals operations
    Args:
        Token (_type_): _description_

    Returns:
        _type_: _description_
    """

    lbp = 0
    regexp = r"[-+]?\d*\.\d+"

    def nud(self, context):
        query = Query()
        query.value = self.text
        return query


class Integer(Token):
    """_summary_
    This Token is used to evaluate Integer operations
    Args:
        Token (_type_): _description_

    Returns:
        _type_: _description_
    """

    lbp = 0
    regexp = r"[-+]?\d+"

    def nud(self, context):
        query = Query()
        query.value = self.text
        return query


def math_logic_check(
    right_side: Union[Query, str], left: Union[Query, str]
) -> Tuple[int, Union[int, float, None]]:
    right_math: Union[int, float, None] = None
    left_math: Union[int, float, None] = None
    if isinstance(right_side, Query):
        if is_float(right_side.value) is True:
            right_math = float(right_side.value)
        else:
            right_math = int(right_side.value)

    if isinstance(left, Query):
        left_side = left.value
        if is_float(left_side) is True:
            left_math = float(left_side)
        else:
            left_math = int(left_side)

    if isinstance(right_side, float):
        right_math = float(right_side)
    if isinstance(right_side, int):
        right_math = int(right_side)
    if isinstance(left, float):
        left_math = float(left)
    if isinstance(left, int):
        left_math = int(left)

    return (right_math, left_math)


class Addition(Token):
    """_summary_
        This Token is used to evaluate Addition operations with the symbol matching this +
    Args:
        Token (_type_): _description_

    Returns:
        _type_: _description_
    """

    regexp = r"\+"
    lbp = 15

    def led(self, left, context):
        query_value = Query()
        right_side = context.expression(self.lbp)
        right_math, left_math = math_logic_check(right_side, left)
        query_value.value = str(left_math + right_math)
        right_side = query_value
        return right_side


class Subtraction(Token):
    """_summary_
    This Token is used to evaluate Subtraction operations with the symbol matching this -

    Args:
        Token (_type_): _description_

    Returns:
        _type_: _description_
    """

    regexp = r"\-"
    lbp = 15

    def led(self, left, context):
        query_value = Query()
        right_side = context.expression(self.lbp)
        right_math, left_math = math_logic_check(right_side, left)
        query_value.value = str(left_math - right_math)
        right_side = query_value
        return right_side


class Division(Token):
    """_summary_
    This Token is used to evaluate Division operations with the symbol matching this /

    Args:
        Token (_type_): _description_

    Returns:
        _type_: _description_
    """

    regexp = r"\/"
    lbp = 15

    def led(self, left, context):
        query_value = Query()
        right_side = context.expression(self.lbp)
        right_math, left_math = math_logic_check(right_side, left)
        query_value.value = str(left_math / right_math)
        right_side = query_value
        return right_side


class Multiplication(Token):
    """_summary_
    This Token is used to evaluate Multiplication operations with the symbol matching this *
    Args:
            Token (_type_): _description_

        Returns:
            _type_: _description_
    """

    regexp = r"\*"
    lbp = 15

    def led(self, left, context) -> Query:
        """_summary_
        This will parse the left and the right strings next to a multiplication sign *
        Args:
            left (_type_): _description_
            context (_type_): _description_

        Returns:
            Query: _description_
        """
        query_value = Query()
        right_side = context.expression(self.lbp)
        right_math, left_math = math_logic_check(right_side, left)
        query_value.value = str(left_math * right_math)
        right_side = query_value
        return right_side


class Expression(Token):
    """_summary_
    This is Expression Token in the  root token most values will hit this token
    Args:
        Token (_type_): _description_

    Returns:
        _type_: _description_
    """

    lbp = 0

    def __init__(self, text: str) -> None:
        self.value = str(text).strip()
        check_keyword(self.value)

    def nud(self, context: Parser) -> Query:
        """What the token evaluates to"""
        query = Query()
        query.value = self.value
        return query


class And(Token):
    """_summary_
    This Token is used to evaluate AND operations with the symbol matching this AND
    Args:
        Token (_type_): _description_

    Returns:
        _type_: _description_
    """

    lbp = 3  # Precedence

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        l_copy_query = build_query_copy(left)

        query.node_type = "AND"
        query.l = l_copy_query

        right_side: Query = context.expression(self.lbp)
        r_copy_query = build_query_copy(right_side)

        query.r = r_copy_query
        return query


class Or(Token):
    """_summary_
    This Token is used to evaluate OR operations with the symbol matching this OR
    Args:
        Token (_type_): _description_

    Returns:
        _type_: _description_
    """

    lbp = 3  # Precedence
    query = Query()

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        l_copy_query = build_query_copy(left)

        query.node_type = "OR"
        query.l = l_copy_query

        right_side: Query = context.expression(self.lbp)
        r_copy_query = build_query_copy(right_side)

        query.r = r_copy_query
        return query


class Eq(Token):
    """_summary_
    This Token is used to evaluate Equal operations with the symbol matching this =
    Args:
        Token (_type_): _description_

    Returns:
        _type_: _description_
    """

    lbp = 10  # Precedence

    def led(self, left: Query, context: Parser) -> Query:
        query = Query()
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query.node_type = "="
        right_side: Query = context.expression(self.lbp)
        if isinstance(right_side.value, str) and right_side.value.find("%") != -1:
            return like_converter(query=query, right_side=right_side, left=left)

        query.l = col(left.value)
        query.r = infer_quote(right_side.value)
        return query


class NotEq(Token):
    """_summary_
    This Token is used to evaluate Not Equal operations with the symbols matching this !=,  <>
    Args:
        Token (_type_): _description_

    Returns:
        _type_: _description_
    """

    lbp = 5  # Precedence

    def led(self, left: Query, context: Parser) -> Query:
        query = Query()
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side: Query = context.expression(self.lbp)
        query.node_type = "!="
        if isinstance(right_side.value, str) and right_side.value.find("%") != -1:
            return like_converter(query=query, right_side=right_side, left=left)
        query.l = col(left.value.strip())
        query.r = infer_quote(right_side.value.strip())
        return query


class GreaterThanEq(Token):
    lbp = 5  # Precedence

    def led(self, left: Query, context: Parser) -> Query:
        query = Query()
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side: Query = context.expression(self.lbp)
        query.node_type = ">="
        query.l = col(left.value.strip())
        query.r = infer_quote(right_side.value.strip())
        return query


class GreaterThan(Token):
    lbp = 5  # Precedence

    def led(self, left: Query, context: Parser) -> Query:
        query = Query()
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side: Query = context.expression(self.lbp)
        query.node_type = ">"
        query.l = col(left.value.strip())
        query.r = infer_quote(right_side.value.strip())
        return query


class LessThanEq(Token):
    lbp = 5  # Precedence

    def led(self, left: Query, context: Parser) -> Query:
        query = Query()
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side: Query = context.expression(self.lbp)
        query.node_type = "<="
        query.l = col(left.value.strip())
        query.r = infer_quote(right_side.value.strip())
        return query


class LessThan(Token):
    lbp = 5  # Precedence

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        query = Query()
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side: Query = context.expression(self.lbp)
        query.node_type = "<"
        query.l = col(left.value.strip())
        query.r = infer_quote(right_side.value.strip())

        return query


class DoubleQuotes(Token):
    lbp = 10  # Precedence

    def nud(self, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        query.value = self.text

        return query


class CommaType(Token):
    lbp = 6

    def led(self, left: Query, context: Parser) -> Query:
        query = Query()
        right_side: Query = context.expression(self.lbp)
        query.value = f"{left.value}{self.text}{right_side.value}"

        return query

    def nud(self, context: Parser) -> Query:
        query = Query()
        query.value = self.text

        return query


class ArrayType(Token):
    lbp = 10

    def nud(self, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        query.value = self.text

        return query


class SingleQuotes(Token):
    lbp = 10  # Precedence

    def nud(self, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        query.value = self.text

        return query


class IN(Token):
    lbp = 5

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        query = Query()
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side: Query = context.expression(self.lbp)
        query.node_type = "IN"
        query.l = col(left.value.strip())
        query.r = infer_quote(right_side.value.strip())
        return query


class LIKE(Token):
    lbp = 5

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        query = Query()
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence

        right_side: Query = context.expression(self.lbp)
        query.node_type = "LIKE"
        query.node_type, right_side = query_type_conversion(
            query.node_type, right_side.value
        )
        query.l = col(left.value.strip())
        query.r = infer_quote(right_side.value.strip())
        return query


class NOT(Token):
    lbp = 4

    def nud(self, context: Parser) -> Query:
        query = Query()
        right_side: Query = context.expression(self.lbp)
        query.node_type = "NOT"
        query.l = right_side
        query.r = infer_quote("")
        return query


class IS(Token):
    lbp = 19

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        right_side: Query = context.expression(self.lbp)

        query.node_type = "IS"
        query.l = col(left.value)
        query.r = infer_quote(right_side.value)

        return query


class IS_NOT(Token):
    lbp = 19

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        query = Query()
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side: Query = context.expression(self.lbp)
        query.node_type = "IS NOT"
        query.l = col(left.value.strip())
        query.r = infer_quote(right_side.value)
        return query


class NOT_IN(Token):
    lbp = 19

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        right_side: Query = context.expression(self.lbp)
        query.node_type = "NOT IN"
        query.l = col(left.value.strip())
        query.r = infer_quote(right_side.value)
        return query


class NOT_LIKE(Token):
    lbp = 19

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        right_side: Query = context.expression(self.lbp)
        query.node_type = "NOT LIKE"
        query.l = col(left.value.strip())
        query.r = infer_quote(right_side.value)
        return query


class From(Token):
    lbp = 2  # Precedence

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        l_copy_query = build_query_copy(left)

        query.node_type = "SUBQUERY"
        query.l = l_copy_query

        right_side: Query = context.expression(self.lbp)
        r_copy_query = build_query_copy(right_side)

        query.r = r_copy_query
        return query


class RightParen(Token):
    """A right parenthesis."""

    def __repr__(self) -> str:  # pragma: no cover
        return "<)>"


class LeftParen(Token):
    """A left parenthesis."""

    match = RightParen

    def nud(self, context: Parser) -> Any:
        # Fetch the next expression
        expr = context.expression()
        pre_token = context.current_token
        # Eat the next token from the flow, and fail if it isn't a right parenthesis.
        context.consume(expect_class=self.match)
        if isinstance(pre_token, RightParen) and hasattr(expr, "value"):
            expr.value = f"({expr.value})"
        return expr

    def __repr__(self) -> Literal["<(>"]:  # pragma: no cover
        return "<(>"


class Limit(Token):
    lbp = 3

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        right_side: Query = context.expression(self.lbp)
        query.node_type = "LIMIT"
        query.r = left
        query.value = right_side.value
        return query


class Offset(Token):
    lbp = 3

    def led(self, left: Query, context: Parser) -> Query:
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        query = Query()
        right_side: Query = context.expression(self.lbp)
        query.node_type = "OFFSET"
        query.r = left
        query.value = right_side.value
        return query


class REPLACE(Token):
    lbp = 19

    def nud(self, context) -> Query:
        query = Query()
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side: Query = context.expression(self.lbp)
        query.node_type = "REPLACE"
        query.l = col(
            ""
        )  # if you're a REPLACE is at the beginning of Q parser, there would be no left
        query.r = right_side  # this Query values
        return query


class AS(Token):
    lbp = 10

    def led(self, left: Query, context) -> Query:
        query = Query()
        # Fetch the expression to the right, stopping at the next boundary
        # of same precedence
        right_side: Query = context.expression(self.lbp)
        query.node_type = "AS"
        query.l = left
        query.r = infer_quote(right_side.value.strip())
        return query


class end_token:
    lbp = 0


lexer = Lexer(with_parens=False)
lexer.register_tokens(
    Integer, Decimal_Number, Addition, Multiplication, Division, Subtraction
)
lexer.register_token(LeftParen, re.compile(r"\("))
lexer.register_token(RightParen, re.compile(r"\)"))
lexer.register_token(
    Expression,
    re.compile(
        r"([-]?[\d]+)|(\"[\w\s]+\")|(?!\*)(?!\+)(?!\/)(?![+-]?([0-9]*[.])?[0-9]+)(\b(?!(\bAND\b))(?!(\bOR\b))(?!(\bNOT\b))(?!(\bLIMIT\b))(?!(\bOFFSET\b))(?!(\bFROM\b))(?!(\bIN\b))(?!(\bLIKE\b))(?!(\bIS\b))(?!(\bAS\b))[a-zA-Z_.\,\*\+\-_\"\'\=\>\<\{\}\[\]\?\\\:@!#$%\^\&\*\(\)\d+]+\b)"
    ),
)


lexer.register_token(DoubleQuotes, re.compile(r'(".*?")'))
lexer.register_token(SingleQuotes, re.compile(r"('.*?')"))
lexer.register_token(ArrayType, re.compile(r"(\[.*?\])"))
lexer.register_token(CommaType, re.compile(r"(\s*,\s*)"))
lexer.register_token(GreaterThan, re.compile(r"(\s+>+\s)"))
lexer.register_token(LessThan, re.compile(r"(\s+<+\s)"))
lexer.register_token(GreaterThanEq, re.compile(r"(\s+>=+\s)"))
lexer.register_token(LessThanEq, re.compile(r"(\s+<=+\s)"))
lexer.register_token(NotEq, re.compile(r"(\s+!=+\s)"))
lexer.register_token(NotEq, re.compile(r"(\s+<>+\s)"))
lexer.register_token(And, re.compile(r"(AND)"))
lexer.register_token(Or, re.compile(r"(OR)"))
lexer.register_token(Eq, re.compile(r"(=)"))
lexer.register_token(IN, re.compile(r"(IN)"))
lexer.register_token(LIKE, re.compile(r"(LIKE)"))
lexer.register_token(From, re.compile(r"(FROM)"))
lexer.register_token(Limit, re.compile(r"(LIMIT)"))
lexer.register_token(Offset, re.compile(r"OFFSET"))
lexer.register_token(NOT, re.compile(r"(NOT)"))
lexer.register_token(IS_NOT, re.compile(r"((IS)\s+(NOT))"))
lexer.register_token(NOT_IN, re.compile(r"((NOT)\s+(IN))"))
lexer.register_token(NOT_LIKE, re.compile(r"((NOT)\s+(LIKE))"))
lexer.register_token(IS, re.compile(r"(IS)"))
# lexer.register_token(FUNCTION, "FUNCTION")
lexer.register_token(AS, "AS")


def simple_parser(text: str) -> "Query":
    return lexer.parse(text)
