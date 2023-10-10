from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query

from cdapython.factories import RESEARCH_SUBJECT_FILE_COUNT
from cdapython.factories.q_factory import AbstractFactory, QFactory
from cdapython.factories.research_subject.research_subject import ResearchSubject

if TYPE_CHECKING:
    from cdapython.Q import Q


class ResearchSubjectFiles(ResearchSubject):
    @property
    def file(self) -> "Q":
        raise NotImplementedError

    @property
    def count(self) -> "Q":
        return QFactory.create_entity(RESEARCH_SUBJECT_FILE_COUNT, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        dry_run: bool,
        async_req: bool,
        offset: int,
        limit: int,
        include_total_count: bool,
        show_term_count: bool,
    ) -> Endpoint:
        return api_instance.research_subject_files_query(
            query=self.query,
            offset=offset,
            dry_run=dry_run,
            limit=limit,
            async_req=async_req,
            include_count=include_total_count,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "ResearchSubjectFiles":
            return ResearchSubjectFiles(q_object.query)
