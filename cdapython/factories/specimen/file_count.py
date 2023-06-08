from typing import TYPE_CHECKING, Optional

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query
from cda_client.model.query_response_data import QueryResponseData

from cdapython.factories.q_factory import AbstractFactory
from cdapython.factories.specimen.file import SpecimenFiles
from cdapython.results.count_result import CountResult
from cdapython.results.result import Result

if TYPE_CHECKING:
    from cdapython.Q import Q


class SpecimenFileCount(SpecimenFiles):
    @property
    def file(self) -> "Q":
        raise NotImplementedError

    @property
    def count(self) -> "Q":
        raise NotImplementedError

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool,
        offset: int,
        page_size: int,
    ) -> Endpoint:
        return api_instance.specimen_file_counts_query(
            query=self.query,
            version=version,
            dry_run=dry_run,
            table=table,
            async_req=async_req,
            offset=offset,
            limit=page_size,
        )

    def _build_result_object(
        self,
        api_response: QueryResponseData,
        offset: int,
        page_size: int,
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        format_type: str = "json",
    ) -> Result:
        return CountResult(
            api_response,
            offset,
            page_size,
            api_instance,
            show_sql,
            show_count,
            format_type,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "SpecimenFileCount":
            return SpecimenFileCount(q_object.query)
