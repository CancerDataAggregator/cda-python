from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query

from cdapython.services.api_count_service import CountsApiService
from cdapython.services.api_files_service import FilesApiService
from cdapython.services.api_service import ApiService


class SubjectQueryService(ApiService):
    @staticmethod
    def call_endpoint(
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool,
    ) -> Endpoint:
        return api_instance.subject_query(
            query, version=version, dry_run=dry_run, table=table, async_req=async_req
        )


class SubjectFilesService(FilesApiService):
    @staticmethod
    def call_endpoint(
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool,
    ) -> Endpoint:
        return api_instance.subject_files_query(
            query, version=version, dry_run=dry_run, table=table, async_req=async_req
        )


class SubjectCountsService(CountsApiService):
    @staticmethod
    def call_endpoint(
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool,
    ) -> Endpoint:
        return api_instance.subject_counts_query(
            query, version=version, dry_run=dry_run, table=table, async_req=async_req
        )
