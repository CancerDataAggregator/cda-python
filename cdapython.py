import pprint
import sys
from typing import Union

import cda_client

__version__ = "2021.3.11"

CDA_API_URL = "https://cda.cda-dev.broadinstitute.org"
table_version = "v3"

pp = pprint.PrettyPrinter(indent=2)


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

    def run(self, offset=0, limit=1000, version=table_version, host=CDA_API_URL, dry_run=False):
        with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=host)
        ) as api_client:
            api_instance = cda_client.QueryApi(api_client)
            query = self.query  # Query | The boolean query
            offset = offset  # int | The number of entries to skip (optional)
            limit = limit  # int | The numbers of entries to return (optional)

            # Execute boolean query
            api_response = api_instance.boolean_query(
                version, query, offset=offset, limit=limit, dry_run=dry_run
            )
            return Result(api_response, offset, limit, version, host)

    def And(self, right: "Q"):
        return Q(self.query, "AND", right.query)

    def Or(self, right: "Q"):
        return Q(self.query, "OR", right.query)

    def From(self, right: "Q"):
        return Q(self.query, "SUBQUERY", right.query)

    def Not(self):
        return Q(self.query, "NOT", None)


class Result:
    """A convenient wrapper around the response object from the CDA service."""

    def __init__(self, api_response, offset, limit, version, host) -> None:
        self._api_response = api_response
        self._offset = offset
        self._limit = limit
        self._version = version
        self._host = host

    def __str__(self) -> str:
        return f"""
Query: {self._api_response.query_sql}
Offset: {self._offset}
Limit: {self._limit}
Count: {self.count}
More pages: {"No" if self.count < self._limit else "Yes"}
"""

    @property
    def sql(self):
        return self._api_response.query_sql

    @property
    def count(self):
        return len(self._api_response.result)

    def __getitem__(self, idx):
        return self._api_response.result[idx]

    def pretty_print(self, idx):
        pp.pprint(self[idx])

    def next_page(self, limit=None):
        if self.count < self._limit:
            raise StopIteration

        _offset = self._offset + self._limit
        _limit = limit or self._limit
        return self._get_result(_offset, _limit)
        
    def prev_page(self, limit=None):
        _offset = self._offset - self._limit
        _offset = max(0, _offset)
        _limit = limit or self._limit
        return self._get_result(_offset, _limit)

    def _get_result(self, _offset, _limit):
        with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=self._host)
        ) as api_client:
            api_instance = cda_client.QueryApi(api_client)
            api_response = api_instance.sql_query(
                self._version, self._api_response.query_sql, offset=_offset, limit=_limit
            )
            return Result(api_response, _offset, _limit, version=self._version, host=self._host)


def columns(version=table_version, host=CDA_API_URL):
    """Get columns names from the database."""
    query = f"SELECT field_path FROM `gdc-bq-sample.cda_mvp.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` WHERE table_name = '{version}'"
    sys.stderr.write(f"{query}\n")
    # Execute boolean query
    with cda_client.ApiClient(
        configuration=cda_client.Configuration(host=host)
    ) as api_client:
        api_instance = cda_client.QueryApi(api_client)
        api_response = api_instance.sql_query(
            version, query, offset=0, limit=10000
        )
        return [list(t.values())[0] for t in api_response.result]


def unique_terms(col_name, system=None, version=table_version, host=CDA_API_URL):
    with cda_client.ApiClient(
        configuration=cda_client.Configuration(host=host)
    ) as api_client:
        api_instance = cda_client.QueryApi(api_client)
        _new_col, _unnest_col = _get_unnest_clause(col_name=col_name)

        if system:
            _new_system, _unnest_system = _get_unnest_clause(col_name='ResearchSubject.identifier.system')
            _unnest = _unnest_col + [item for item in _unnest_system if item not in _unnest_col]
            _where_clause = f" WHERE {_new_system}=\"{system}\""
        else:
            _unnest = _unnest_col
            _where_clause = ''
        if _unnest:
            _unnest_clause = f", {','.join(_unnest)}"
        else:
            _unnest_clause = ''

        query = f"SELECT DISTINCT({_new_col}) FROM `gdc-bq-sample.cda_mvp.{version}`" \
                f"{_unnest_clause}{_where_clause} ORDER BY {_new_col}"

        sys.stderr.write(f"{query}\n")

        # Execute boolean query
        api_response = api_instance.sql_query(
            version, query, offset=0, limit=10000
        )
        return [list(t.values())[0] for t in api_response.result]


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
