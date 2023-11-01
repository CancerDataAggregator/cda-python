from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint


from cdapython.factories import DIAGNOSIS_COUNT
from cdapython.factories.entity import Entity
from cdapython.factories.q_factory import AbstractFactory, QFactory

if TYPE_CHECKING:
    from cdapython.Q import Q


class Diagnosis(Entity):
    @property
    def count(self) -> "Q":
        return QFactory.create_entity(DIAGNOSIS_COUNT, self)

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
        return api_instance.diagnosis_query(
            query=self.query,
            dry_run=dry_run,
            offset=offset,
            limit=limit,
            async_req=async_req,
            include_count=include_total_count,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "Diagnosis":
            return Diagnosis(q_object.query)
