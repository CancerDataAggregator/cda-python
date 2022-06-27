from typing import TYPE_CHECKING
from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query
from cdapython.factories import SUBJECT_FILE_COUNT
from cdapython.factories.q_factory import AbstractFactory, QFactory
from cdapython.factories.subject.subject import Subject

if TYPE_CHECKING:
    from cdapython.Q import Q


class SubjectFiles(Subject):
    @property
    def file(self) -> "Q":
        raise NotImplementedError

    @property
    def count(self) -> "Q":
        return QFactory.create_entity(SUBJECT_FILE_COUNT, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool,
    ) -> Endpoint:
        return api_instance.subject_files_query(
            query, version=version, dry_run=dry_run, table=table, async_req=async_req
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "SubjectFiles":
            return SubjectFiles(q_object.query)
