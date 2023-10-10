from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query

from cdapython.factories import SUBJECT_COUNT, SUBJECT_FILE
from cdapython.factories.entity import Entity
from cdapython.factories.q_factory import AbstractFactory, QFactory

if TYPE_CHECKING:
    from cdapython.Q import Q


class Subject(Entity):
    @property
    def file(self) -> "Q":
        return QFactory.create_entity(SUBJECT_FILE, self)

    @property
    def count(self) -> "Q":
        return QFactory.create_entity(SUBJECT_COUNT, self)

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
        return api_instance.subject_query(
            query=self.query,
            dry_run=dry_run,
            async_req=async_req,
            offset=offset,
            limit=limit,
            include_count=include_total_count,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "Subject":
            return Subject(q_object.query)
