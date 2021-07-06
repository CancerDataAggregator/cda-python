import cda_client
import sys
from cda_client.api.query_api import QueryApi
from .Result import get_query_result
from .constantVariables import table_version,CDA_API_URL
from ._get_unnest_clause import _get_unnest_clause

def unique_terms(col_name, system=''):
    with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=CDA_API_URL)
    ) as api_client:
        system = str(system) 
        api_instance = QueryApi(api_client)
        api_response = api_instance.unique_values(version=table_version, body=col_name, system=system)
        # Execute query
        query_result = get_query_result(api_instance, api_response.query_id, 0, 1000)
        return [list(t.values())[0] for t in query_result]