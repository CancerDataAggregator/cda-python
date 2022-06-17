from typing import TYPE_CHECKING, Optional
from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query
from cdapython.factories import SUBJECT_FILE_COUNT
from cdapython.factories.q_factory import QFactory
from cdapython.factories.subject.subject import Subject
from cdapython.results.count_result import CountResult
from cdapython.results.result import Result
from cda_client.model.query_response_data import QueryResponseData

if TYPE_CHECKING:
    from cdapython.Q import Q


class SubjectCount(Subject):
    @property
    def file(self) -> "Q":
        return QFactory.create_entity(SUBJECT_FILE_COUNT, self.query)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool
    ) -> Endpoint:
        return api_instance.subject_counts_query(
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

    class Factory:
        @staticmethod
        def create(q_object):
            return SubjectCount(q_object.query)
