from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint

from cdapython.factories import SPECIMEN_COUNT, SPECIMEN_FILE
from cdapython.factories.entity import Entity
from cdapython.factories.q_factory import AbstractFactory, QFactory

if TYPE_CHECKING:
    from cdapython.Q import Q


class Specimen(Entity):
    @property
    def file(self) -> "Q":
        return QFactory.create_entity(SPECIMEN_FILE, self)

    @property
    def count(self) -> "Q":
        return QFactory.create_entity(SPECIMEN_COUNT, self)

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
        return api_instance.specimen_query(
            query=self.query,
            dry_run=dry_run,
            async_req=async_req,
            offset=offset,
            limit=limit,
            include_count=include_total_count,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "Specimen":
            return Specimen(q_object.query)
