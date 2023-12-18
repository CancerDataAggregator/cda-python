from typing import TYPE_CHECKING, Optional

from cda_client.api.query_api import QueryApi
from cda_client.model.paged_response_data import PagedResponseData

from cdapython.factories.entity import Entity
from cdapython.factories.q_factory import AbstractFactory

if TYPE_CHECKING:
    from cdapython.Q import Q


class BooleanQuery(Entity):
    def _call_endpoint(
        self,
        api_instance: QueryApi,
        dry_run: bool,
        offset: int,
        limit: int,
        async_req: bool,
        include_total_count: bool,
        show_counts: Optional[bool],
    ) -> PagedResponseData:
        """

        Args:
            api_instance (QueryApi): _description_
            dry_run (bool): _description_
            offset (int) The number of entries to skip.:
            limit (int): _description_
            async_req (bool): _description_
            include_total_count (bool): _description_
            show_counts (Optional[bool]):  Show the number of occurrences for each value

        Returns:
            PagedResponseData: _description_
        """
        print("ran boolean_query.py _call_endpoint")
        return api_instance.boolean_query(
            query=self.query,
            dry_run=dry_run,
            offset=offset,
            limit=limit,
            async_req=async_req,
            include_count=include_total_count,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "BooleanQuery":
            print("ran boolean_query.py create")
            return BooleanQuery(q_object.query)