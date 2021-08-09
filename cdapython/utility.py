import cda_client
import sys
from cda_client.api.query_api import QueryApi
from cdapython.Result import get_query_result
from cdapython.constantVariables import table_version,CDA_API_URL


def unique_terms(col_name, system='',limit=1000) -> list:
    with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=CDA_API_URL)
    ) as api_client:
        api_instance = QueryApi(api_client)
        api_response = api_instance.unique_values(version=table_version, body=col_name, system=str(system))
        # Execute query
        query_result = get_query_result(api_instance, api_response.query_id, 0, limit)
        return [list(t.values())[0] for t in query_result]


def columns(version=table_version, host=CDA_API_URL) -> list:
    """Get columns names from the database."""
    query = f"SELECT field_path FROM `gdc-bq-sample.cda_mvp.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` WHERE table_name = '{version}'"
    sys.stderr.write(f"{query}\n")
    # Execute query
    with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=host)
    ) as api_client:
        api_instance = QueryApi(api_client)
        api_response = api_instance.sql_query(query)
        query_result = get_query_result(api_instance, api_response.query_id, 0, 1000)
        return [list(t.values())[0] for t in query_result]