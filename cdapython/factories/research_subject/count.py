from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint

from cda_client.model.query_response_data import QueryResponseData

from cdapython.factories import RESEARCH_SUBJECT_FILE_COUNT
from cdapython.factories.q_factory import AbstractFactory, QFactory
from cdapython.factories.research_subject.research_subject import ResearchSubject
from cdapython.results.count_result import CountResult
from cdapython.results.result import Result

if TYPE_CHECKING:
    from cdapython.Q import Q


class ResearchSubjectCount(ResearchSubject):
    @property
    def file(self) -> "Q":
        print("ran research_subject/count.py file")
        return QFactory.create_entity(RESEARCH_SUBJECT_FILE_COUNT, self)

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
        print("ran research_subject/count.py _call_endpoint")
        return api_instance.research_subject_counts_query(
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
        print("ran research_subject/count.py _build_result_object")
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
        def create(q_object: "Q") -> "ResearchSubjectCount":
            print("ran research_subject/count.py create")
            return ResearchSubjectCount(q_object.query)
