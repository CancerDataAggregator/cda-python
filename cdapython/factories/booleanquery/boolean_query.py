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
        Call the endpoint to start the job for data collection.
        Args:
            api_instance (QueryApi): _description_
            dry_run (bool): _description_
            offset (int): _description_
            limit (int): _description_
            async_req (bool): _description_
            include_total_count (bool): _description_
            show_term_frequency (Optional[bool]): _description_

        Returns:
            PagedResponseData: _description_
        """
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
            return BooleanQuery(q_object.query)
