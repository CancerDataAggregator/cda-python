from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query

from cdapython.factories import SPECIMEN_FILE_COUNT
from cdapython.factories.q_factory import AbstractFactory, QFactory
from cdapython.factories.specimen.specimen import Specimen

if TYPE_CHECKING:
    from cdapython.Q import Q


class SpecimenFiles(Specimen):
    @property
    def file(self) -> "Q":
        raise NotImplementedError

    @property
    def count(self) -> "Q":
        return QFactory.create_entity(SPECIMEN_FILE_COUNT, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        query: Query,
        dry_run: bool,
        async_req: bool,
        limit: int,
        offset: int,
        include_total_count: bool,
        show_term_count: bool,
    ) -> Endpoint:
        return api_instance.specimen_files_query(
            query=query,
            dry_run=dry_run,
            limit=limit,
            offset=offset,
            include_total_count=include_total_count,
            async_req=async_req,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "SpecimenFiles":
            return SpecimenFiles(q_object.query)
