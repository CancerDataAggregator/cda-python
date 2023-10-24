from typing import TYPE_CHECKING, Optional

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint

from cdapython.factories.entity import Entity
from cdapython.factories.q_factory import AbstractFactory

if TYPE_CHECKING:
    from cdapython.Q import Q


class UniqueTerms(Entity):
    def _call_endpoint(
        self,
        api_instance: QueryApi,
        dry_run: bool,
        async_req: bool,
        offset: int,
        limit: int,
        show_term_count: Optional[bool],
        include_total_count: bool,
        system: Optional[str] = "",
    ) -> Endpoint:
        system = self._get_system()
        if system:
            return api_instance.unique_values(
                body=self.query.value,
                system=system,
                count=show_term_count,
                async_req=async_req,
                offset=offset,
                limit=limit,
                include_count=include_total_count,
            )
        else:
            return api_instance.unique_values(
                body=self.query.value,
                system=system,
                count=show_term_count,
                async_req=async_req,
                offset=offset,
                limit=limit,
                include_count=include_total_count,
            )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "UniqueTerms":
            Q_unique = UniqueTerms(q_object.query)
            Q_unique.set_raw_string(q_object.get_raw_string())
            return Q_unique
