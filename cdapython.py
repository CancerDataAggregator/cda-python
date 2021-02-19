from typing import Union, List
import sys

import cda_client
from cda_client.rest import ApiException

__version__ = "2021.2.19"

CDA_API_URL = "https://cda.cda-dev.broadinstitute.org"


def Col(col_name) -> cda_client.Query:
    return cda_client.Query(node_type="column", value=col_name)


def Quoted(quoted_val) -> cda_client.Query:
    return cda_client.Query(node_type="quoted", value=quoted_val)


def Unquoted(val) -> cda_client.Query:
    return cda_client.Query(node_type="unquoted", value=val)


def infer_quote(val: Union[int, float, str, "Q", cda_client.Query]) -> cda_client.Query:
    if isinstance(val, (Q, cda_client.Query)):
        return val
    elif isinstance(val, str):
        if val.startswith('"') and val.endswith('"'):
            return Quoted(val[1:-1])
        else:
            return Unquoted(val)
    else:
        return Unquoted(val)


class Q:
    def __init__(self, *args) -> None:
        self.query = cda_client.Query()

        if len(args) == 1:
            _l, _op, _r = args[0].split(" ", 2)
            _l = Col(_l)
            _r = infer_quote(_r)
        elif len(args) != 3:
            raise RuntimeError(
                "Require one or three arguments. Please see documentation."
            )
        else:
            _l = infer_quote(args[0])
            _op = args[1]
            _r = infer_quote(args[2])

        self.query.node_type = _op
        self.query.l = _l
        self.query.r = _r

    def run(self, offset=0, limit=None, version="v1", host=CDA_API_URL):
        with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=host)
        ) as api_client:
            api_instance = cda_client.QueryApi(api_client)
            query = self.query  # Query | The boolean query
            offset = offset  # int | The number of entries to skip (optional)
            limit = limit  # int | The numbers of entries to return (optional)

            # Execute boolean query
            api_response = api_instance.boolean_query(
                version, query, offset=offset, limit=limit
            )
            return api_response

    def And(self, right: "Q"):
        return Q(self.query, "AND", right.query)

    def Or(self, right: "Q"):
        return Q(self.query, "OR", right.query)


def unique_terms(col_name, version="v1", host=CDA_API_URL):
    with cda_client.ApiClient(
        configuration=cda_client.Configuration(host=host)
    ) as api_client:
        api_instance = cda_client.QueryApi(api_client)
        _new_col, _unnest = _get_unnest_clause(col_name=col_name)

        query = f"SELECT DISTINCT({_new_col}) FROM `gdc-bq-sample.cda_mvp.{version}`, {','.join(_unnest)}"
        sys.stderr.write(f"{query}\n")

        # Execute boolean query
        api_response = api_instance.sql_query(
            version, query, offset=0, limit=10000
        )
        return api_response


# column ->
# SELECT DISTINCT(column)

# D.column ->
# SELECT DISTINCT(_D.column) FROM TABLE, UNNEST(D) AS _D

# A.B.C.D.column ->
# SELECT DISTINCT(_D.column) FROM TABLE, UNNEST(A) AS _A, UNNEST(_A.B) AS _B, UNNEST(_B.C) AS _C, UNNEST(_C.D) AS _D
def _get_unnest_clause(col_name):
    _new_col, _unnest = col_name, []
    c = col_name.split(".")
    if len(c) > 1:
        _new_col = f"_{c[-2]}.{c[-1]}"
        _unnest = [f"UNNEST({c[0]}) AS _{c[0]}"]
        for n in range(1, len(c) - 1):
            _unnest += [f"UNNEST(_{c[n-1]}.{c[n]}) AS _{c[n]}"]
        
    return (_new_col, _unnest)
