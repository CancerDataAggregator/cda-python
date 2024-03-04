from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint

from cdapython.factories import RESEARCH_SUBJECT_COUNT, RESEARCH_SUBJECT_FILE
from cdapython.factories.entity import Entity
from cdapython.factories.q_factory import AbstractFactory, QFactory

if TYPE_CHECKING:
    from cdapython.Q import Q


class ResearchSubject(Entity):
    @property
    def file(self) -> "Q":
        print("ran research_subject/research_subject.py file")
        return QFactory.create_entity(RESEARCH_SUBJECT_FILE, self)

    @property
    def count(self) -> "Q":
        print("ran research_subject/research_subject.py count")
        return QFactory.create_entity(RESEARCH_SUBJECT_COUNT, self)

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
        print("ran research_subject/research_subject.py _call_endpoint")

        # DEBUG: Output query being sent to API.

        print( self.to_json() )

        return api_instance.research_subject_query(
            query=self.query,
            dry_run=dry_run,
            offset=offset,
            limit=limit,
            async_req=async_req,
            include_count=include_total_count,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "ResearchSubject":
            print("ran research_subject/research_subject.py create")
            return ResearchSubject(q_object.query)
