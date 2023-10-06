from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query

from cdapython.factories import RESEARCH_SUBJECT_COUNT, RESEARCH_SUBJECT_FILE
from cdapython.factories.entity import Entity
from cdapython.factories.q_factory import AbstractFactory, QFactory

if TYPE_CHECKING:
    from cdapython.Q import Q


class ResearchSubject(Entity):
    @property
    def file(self) -> "Q":
        return QFactory.create_entity(RESEARCH_SUBJECT_FILE, self)

    @property
    def count(self) -> "Q":
        return QFactory.create_entity(RESEARCH_SUBJECT_COUNT, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        dry_run: bool,
        async_req: bool,
        offset: int,
        limit: int,
    ) -> Endpoint:
        return api_instance.research_subject_query(
            query=self.query,
            dry_run=dry_run,
            offset=offset,
            limit=limit,
            async_req=async_req,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "ResearchSubject":
            return ResearchSubject(q_object.query)
