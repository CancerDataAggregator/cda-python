from typing import TYPE_CHECKING
from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query
from cdapython.factories.entity import Entity
from cdapython.factories import FILE_COUNT
from cdapython.factories.q_factory import AbstractFactory, QFactory

if TYPE_CHECKING:
    from cdapython.Q import Q


class File(Entity):
    @property
    def count(self) -> "Q":
        return QFactory.create_entity(FILE_COUNT, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool
    ) -> Endpoint:
        return api_instance.files(
            query, version=version, dry_run=dry_run, table=table, async_req=async_req
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object):
            subject = File(q_object.query)
            return subject
