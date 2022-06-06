from multiprocessing.pool import ApplyResult
from time import sleep
from typing import Optional

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query

from cdapython.results.count_result import CountResult
from cdapython.services.api_service import ApiService


class CountsApiService(ApiService):
    @staticmethod
    def call_endpoint(
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool,
    ) -> Endpoint:
        return api_instance.global_counts(
            query, version=version, dry_run=dry_run, table=table, async_req=async_req
        )

    @staticmethod
    def get_query_result(
        api_instance: QueryApi,
        query_id: str,
        offset: Optional[int],
        limit: Optional[int],
        async_req: Optional[bool],
        pre_stream: bool = True,
        show_sql: bool = True,
        show_count: bool = True,
        format_type: str = "json",
    ) -> Endpoint:
        while True:
            response = api_instance.query(
                id=query_id,
                offset=offset,
                limit=limit,
                async_req=async_req,
                _preload_content=pre_stream,
                _check_return_type=False,
            )

            if isinstance(response, ApplyResult):
                response = response.get()

            sleep(2.5)
            if response.total_row_count is not None:
                return CountResult(
                    response,
                    query_id,
                    offset,
                    limit,
                    api_instance,
                    show_sql,
                    show_count,
                    format_type,
                )
