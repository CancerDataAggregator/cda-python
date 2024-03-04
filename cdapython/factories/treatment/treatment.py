from typing import TYPE_CHECKING

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query

from cdapython.factories import TREATMENT_COUNT
from cdapython.factories.entity import Entity
from cdapython.factories.q_factory import AbstractFactory, QFactory

if TYPE_CHECKING:
    from cdapython.Q import Q


class Treatment(Entity):
    @property
    def count(self) -> "Q":
        print("ran treatment/treatment.py count")
        return QFactory.create_entity(TREATMENT_COUNT, self)

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
        print("ran treatment/treatment.py _call_endpoint")

        # DEBUG: Output query being sent to API.

        print( self.to_json() )

        return api_instance.treatments_query(
            query=self.query,
            dry_run=dry_run,
            async_req=async_req,
            offset=offset,
            limit=limit,
            include_count=include_total_count,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "Treatment":
            print("ran treatment/treatment.py create")
            return Treatment(q_object.query)
