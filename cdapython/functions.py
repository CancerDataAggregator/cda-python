from typing import Optional
from cda_client.model.query import Query


def col(col_name: Optional[str]) -> Query:
    return Query(node_type="column", value=col_name)


def Quoted(quoted_val: Optional[str]) -> Query:
    return Query(node_type="quoted", value=quoted_val)


def Unquoted(val: Optional[str]) -> Query:
    return Query(node_type="unquoted", value=val)
