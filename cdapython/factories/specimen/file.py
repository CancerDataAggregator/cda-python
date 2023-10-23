"""
This module holds the SpecimenFiles class
    
"""
from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint

from cdapython.factories import SPECIMEN_FILE_COUNT
from cdapython.factories.q_factory import AbstractFactory, QFactory
from cdapython.factories.specimen.specimen import Specimen

if TYPE_CHECKING:
    from cdapython.Q import Q


class SpecimenFiles(Specimen):
    """
    This factory calls the specimen file endpoint
    Args:
        Specimen (_type_): _description_

    Raises:
        NotImplementedError: _description_

    Returns:
        _type_: _description_
    """

    @property
    def file(self) -> "Q":
        raise NotImplementedError

    @property
    def count(self) -> "Q":
        return QFactory.create_entity(SPECIMEN_FILE_COUNT, self)

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
        return api_instance.specimen_files_query(
            query=self.query,
            dry_run=dry_run,
            limit=limit,
            offset=offset,
            include_count=include_total_count,
            async_req=async_req,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "SpecimenFiles":
            return SpecimenFiles(q_object.query)
