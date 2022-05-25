from cdapython.services.api_count_service import CountsApiService
from cdapython.services.api_service import ApiService
from cda_client.api.query_api import QueryApi
from cda_client.model.query import Query


class DiagnosisQueryService(ApiService):
  @staticmethod
  def call_endpoint(api_instance: QueryApi,
                    query: Query,
                    version: str,
                    dry_run: bool,
                    table: str,
                    async_req: bool):
    return api_instance.diagnosis_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )

class DiagnosisCountsService(CountsApiService):
  @staticmethod
  def call_endpoint(api_instance: QueryApi,
                    query: Query,
                    version: str,
                    dry_run: bool,
                    table: str,
                    async_req: bool):
    return api_instance.diagnosis_counts_query(
        query, version=version, dry_run=dry_run, table=table, async_req=async_req
    )
