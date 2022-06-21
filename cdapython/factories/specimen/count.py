from typing import TYPE_CHECKING, Optional
from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query
from cdapython.factories import SPECIMEN_FILE_COUNT
from cdapython.factories.q_factory import AbstractFactory, QFactory
from cdapython.factories.specimen.specimen import Specimen
from cdapython.results.count_result import CountResult
from cdapython.results.result import Result
from cda_client.model.query_response_data import QueryResponseData

if TYPE_CHECKING:
    from cdapython.Q import Q


class SpecimenCount(Specimen):
    @property
    def file(self) -> "Q":
        return QFactory.create_entity(SPECIMEN_FILE_COUNT, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool
    ) -> Endpoint:
        return api_instance.specimen_counts_query(
            query, version=version, dry_run=dry_run, table=table, async_req=async_req
        )

    def _build_result_object(
        self,
        api_response: QueryResponseData,
        query_id: str,
        offset: Optional[int],
        limit: Optional[int],
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        format_type: str = "json",
    ) -> Result:
        return CountResult(
            api_response,
            query_id,
            offset,
            limit,
            api_instance,
            show_sql,
            show_count,
            format_type,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object):
            return SpecimenCount(q_object.query)
