import pprint
import sys
from typing import Union

import cda_client
from cda_client.api.query_api import QueryApi
from cda_client.model.query import Query

__version__ = "2021.6.15"

#CDA_API_URL = "https://cda.cda-dev.broadinstitute.org"
CDA_API_URL = "http://localhost:8080"
table_version = "v3"

pp = pprint.PrettyPrinter(indent=2)


# these methods may be better expressed as subclasses of Query
def Col(col_name) -> Query:
    return Query(node_type="column", value=col_name)


def Quoted(quoted_val) -> Query:
    return Query(node_type="quoted", value=quoted_val)


def Unquoted(val) -> Query:
    return Query(node_type="unquoted", value=val)


def infer_quote(val: Union[int, float, str, "Q", Query]) -> Query:
    if isinstance(val, (Q, Query)):
        return val
    elif isinstance(val, str) and val.startswith('"') and val.endswith('"'):
        return Quoted(val[1:-1])
    else:
        return Unquoted(val)


def get_query_result(api_instance, query_id, offset, limit):
    while True:
        response = api_instance.query(id=query_id, offset=offset, limit=limit)
        if response.total_row_count is not None:
            return Result(response, query_id, offset, limit, api_instance)


class Q:
    def __init__(self, *args) -> None:
        self.query = Query()

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
            api_instance = QueryApi(api_client)
            # Execute boolean query
            api_response = api_instance.boolean_query(self.query, version=version, dry_run=dry_run)
            if dry_run is True:
                return api_response
            return get_query_result(api_instance, api_response.query_id, offset, limit)

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

    def __init__(self, api_response, query_id, offset, limit, api_instance) -> None:
        self._api_response = api_response
        self._query_id = query_id
        self._offset = offset
        self._limit = limit
        self._api_instance = api_instance

    def __str__(self) -> str:
        return f"""
Query: {self.sql}
Offset: {self._offset}
Count: {self.count}
Total Row Count: {self.total_row_count}
More pages: {self.has_next_page}
"""

    @property
    def sql(self):
        return self._api_response.query_sql

    @property
    def count(self):
        return len(self._api_response.result)

    @property
    def total_row_count(self):
        return self._api_response.total_row_count

    @property
    def has_next_page(self):
        return (self._offset + self._limit) <= self.total_row_count

    def __getitem__(self, idx):
        return self._api_response.result[idx]

    def pretty_print(self, idx):
        pp.pprint(self[idx])

    def next_page(self, limit=None):
        if not self.has_next_page:
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
        return get_query_result(self._api_instance, self._query_id, _offset, _limit)


def columns(version=table_version, host=CDA_API_URL):
    """Get columns names from the database."""
    query = f"SELECT field_path FROM `gdc-bq-sample.cda_mvp.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`"
    sys.stderr.write(f"{query}\n")
    # Execute query
    with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=host)
    ) as api_client:
        api_instance = QueryApi(api_client)
        api_response = api_instance.sql_query(query)
        query_result = get_query_result(api_instance, api_response.query_id, 0, 1000)
        return [list(t.values())[0] for t in query_result]


def unique_terms(col_name, system=None, version=table_version, host=CDA_API_URL):
    with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=host)
    ) as api_client:
        api_instance = QueryApi(api_client)
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

        # Execute query
        api_response = api_instance.sql_query(query)
        query_result = get_query_result(api_instance, api_response.query_id, 0, 1000)
        return [list(t.values())[0] for t in query_result]


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
            _unnest += [f"UNNEST(_{c[n - 1]}.{c[n]}) AS _{c[n]}"]

    return _new_col, _unnest
