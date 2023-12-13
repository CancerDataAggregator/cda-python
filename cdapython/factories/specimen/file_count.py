from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
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
        print("ran specimen/file_count.py file")
        raise NotImplementedError

    @property
    def count(self) -> "Q":
        print("ran specimen/file_count.py count")
        raise NotImplementedError

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        dry_run: bool,
        offset: int,
        limit: int,
        async_req: bool,
        include_total_count: bool,
        show_counts: bool,
    ) -> Endpoint:
        print("ran specimen/file_count.py _call_endpoint")
        return api_instance.specimen_file_counts_query(
            query=self.query,
            dry_run=dry_run,
            async_req=async_req,
        )

    def _build_result_object(
        self,
        api_response: QueryResponseData,
        offset: int,
        limit: int,
        api_instance: QueryApi,
        show_sql: bool,
        q_object: "Q",
        format_type: str = "json",
    ) -> Result:
        print("ran specimen/file_count.py _build_result_object")
        return CountResult(
            api_response=api_response,
            offset=offset,
            limit=limit,
            api_instance=api_instance,
            show_sql=show_sql,
            format_type=format_type,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "SpecimenFileCount":
            print("ran specimen/file_count.py create")
            return SpecimenFileCount(q_object.query)
