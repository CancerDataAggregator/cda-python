from os import path
from ssl import get_default_verify_paths
from typing import TYPE_CHECKING, Any, Optional, Tuple, Union, overload

from cda_client.model.query import Query
from typing_extensions import Literal

from cdapython.dataclasses.querystr import QueryStr
from cdapython.utils.ConversionMap import CONVERSIONMAP

if TYPE_CHECKING:
    from cdapython.Q import Q


def col(col_name: Optional[Union[str, Query]]) -> Query:
    return Query(node_type="column", value=col_name)


def quoted(quoted_val: Optional[Union[str, Query]]) -> Query:
    return Query(node_type="quoted", value=quoted_val)


def unquoted(val: Optional[Union[str, Query]]) -> Query:
    return Query(node_type="unquoted", value=val)


def find_ssl_path() -> bool:
    """[summary]
    This will look in your local computer for a ssl pem file and
    return True or False if the file is there.
    if value is False Q will accept any TLS certificate presented by a server,
    and will ignore hostname mismatches and expired certificates
    Returns:
        bool: [description]
    """
    openssl_cafile: str
    openssl_dir: str
    openssl_dir, openssl_cafile = path.split(get_default_verify_paths().openssl_cafile)
    check: bool = True

    if not path.exists(openssl_dir):
        check = False

    if openssl_cafile.find("pem") == -1:
        check = False

    return check


def backwards_comp(value: str) -> str:
    """_summary_
        This is a function will look up a string value in a dictionary
    Args:
        value (str): _description_

    Returns:
        str: _description_
    """
    if isinstance(value, str) and value in CONVERSIONMAP:
        tmp_l: str = CONVERSIONMAP[value]
        print(
            f"""
                This Value {value} has been deprecated but will be converted
                it for you in the background please use the new value {tmp_l}
                """
        )
        return tmp_l
    return value


@overload
def infer_quote(val: str) -> str:
    pass


@overload
def infer_quote(val: Query) -> Query:
    pass


def infer_quote(val: Any) -> Union[Query, QueryStr]:
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
        tmp = Query()
        tmp.node_type = "quoted"
        tmp.value = _r
        tmp_str = "NOT " if _op == "!=" or _op == "<>" else ""
        return (f"{tmp_str}LIKE", tmp)

    if _r.find("LIKE") != -1:
        tmp = Query()
        tmp.node_type = "quoted"
        tmp.value = _r
        return ("LIKE", tmp)

    return (_op, _r)
