from typing import TYPE_CHECKING, Optional
from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query
from cdapython.factories.q_factory import AbstractFactory
from cdapython.factories.research_subject.file import ResearchSubjectFiles
from cdapython.results.result import Result
from cdapython.results.count_result import CountResult
from cda_client.model.query_response_data import QueryResponseData

if TYPE_CHECKING:
    from cdapython.Q import Q


class ResearchSubjectFileCount(ResearchSubjectFiles):
    @property
    def file(self) -> "Q":
        raise NotImplementedError

    @property
    def count(self) -> "Q":
        raise NotImplementedError

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool,
    ) -> Endpoint:
        return api_instance.research_subject_file_counts_query(
            query=query,
            version=version,
            dry_run=dry_run,
            table=table,
            async_req=async_req,
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
        def create(q_object: "Q") -> "ResearchSubjectFileCount":
            return ResearchSubjectFileCount(q_object.query)
