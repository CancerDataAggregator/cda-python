from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query_response_data import QueryResponseData

from cdapython.factories import SPECIMEN_FILE_COUNT
from cdapython.factories.q_factory import AbstractFactory, QFactory
from cdapython.factories.specimen.specimen import Specimen
from cdapython.results.count_result import CountResult
from cdapython.results.result import Result

if TYPE_CHECKING:
    from cdapython.Q import Q


class SpecimenCount(Specimen):
    @property
    def file(self) -> "Q":
        return QFactory.create_entity(SPECIMEN_FILE_COUNT, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        dry_run: bool,
        offset: int,
        limit: int,
        async_req: bool,
        include_total_count: bool,
        show_term_count: bool,
    ) -> Endpoint:
        return api_instance.specimen_counts_query(
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
        show_count: bool,
        q_object: "Q",
        format_type: str = "json",
    ) -> Result:
        return CountResult(
            api_response=api_response,
            offset=offset,
            limit=limit,
            api_instance=api_instance,
            show_sql=show_sql,
            show_count=show_count,
            format_type=format_type,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "SpecimenCount":
            return SpecimenCount(q_object.query)
