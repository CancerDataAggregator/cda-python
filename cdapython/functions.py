from typing import Tuple, Union, overload

from cda_client.model.query import Query
from typing_extensions import Literal

from cdapython.dataclasses_Q.querystr import QueryStr


def col(col_name: Union[str, Query, None]) -> Query:
    return Query(node_type="column", value=col_name)


def quoted(quoted_val: Union[str, Query, None]) -> Query:
    return Query(node_type="quoted", value=quoted_val)


def unquoted(val: Union[str, Query, None]) -> Query:
    return Query(node_type="unquoted", value=val)


@overload
def infer_quote(val: str) -> str:
    """_summary_
    this is a overload for a str typechecking
    Args:
        val (str): _description_

    Returns:
        str: _description_
    """
    pass


@overload
def infer_quote(val: Query) -> Query:
    """_summary_
    this is a overload for a Query for typechecking
    Args:
        val (Query): _description_

    Returns:
        Query: _description_
    """
    pass


@overload
def infer_quote(val: QueryStr) -> QueryStr:
    """_summary_
    this is a overload for a Query for typechecking
    Args:
        val (Query): _description_

    Returns:
        Query: _description_
    """
    pass


def infer_quote(val: Union[str, Query, QueryStr]) -> Union[Query, QueryStr, str]:
    """[summary]
    Handles Strings With quotes by checking the value type
    Args:
        val (Union[str,"Q",Query): [description]

    Returns:
        Query: [description]
    """
    if isinstance(val, QueryStr):
        return val
    if isinstance(val, Query):
        return val

    if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
        return quoted(val[1:-1])

    if isinstance(val, str) and val.startswith("'") and val.endswith("'"):
        return quoted(val[1:-1])
    return unquoted(val)


def query_type_conversion(
    _op: str, _r: Union[str, Query, QueryStr]
) -> Union[
    Tuple[Literal["LIKE"], QueryStr], Tuple[Literal["LIKE"], Query], Tuple[str, str]
]:
    """_summary_
        This is for query type conversion in looking operator
    Args:
        _op (str): _description_
        _r (str): _description_

    Returns:
        (tuple[Literal['LIKE'], Query] | tuple[str, str])
    """
    if _r.find("%") != -1:
        tmp: Query = Query()
        tmp.node_type = "quoted"
        tmp.value = _r
        tmp_str: Literal["NOT ", ""] = "NOT " if _op == "!=" or _op == "<>" else ""
        return (f"{tmp_str}LIKE", tmp)

    if _r.find("LIKE") != -1:
        tmp: Query = Query()
        tmp.node_type = "quoted"
        tmp.value = _r
        return ("LIKE", tmp)

    return (_op, _r)
