from constantVariables import table_version,CDA_API_URL
import get_query_result
import cda_client,sys
from cda_client.api.query_api import QueryApi
from cda_client.model.query import Query

def columns(version=table_version, host=CDA_API_URL):
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