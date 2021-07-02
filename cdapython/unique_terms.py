import sys
import cda_client
from constantVariables import table_version
from cda_client import QueryApi
from ._get_unnest_clause import _get_unnest_clause
from .get_query_result import get_query_result
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