from typing import TYPE_CHECKING, Optional

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query
from cda_client.model.query_response_data import QueryResponseData

from cdapython.factories.entity import Entity
from cdapython.factories.q_factory import AbstractFactory
from cdapython.results.count_result import CountResult
from cdapython.results.result import Result

if TYPE_CHECKING:
    from cdapython.Q import Q


class FileCount(Entity):
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
        print("ran factories/file_count.py _call_endpoint")

        # DEBUG: Output query being sent to API.

        print( self.to_json() )

        return api_instance.file_counts_query(
            query=self.query,
            dry_run=dry_run,
            async_req=async_req,
        )

    def _build_result_object(
        self,
        api_response: QueryResponseData,
        offset: int,
        limit: int,
        api_instance: QueryApi,
        show_sql: bool,
        q_object: "Q",
        format_type: str = "json",
    ) -> Result:
        print("ran factories/file_count.py _build_result_object")
        return CountResult(
            api_response=api_response,
            offset=offset,
            limit=limit,
            api_instance=api_instance,
            show_sql=show_sql,
            format_type=format_type,
        )

    class Factory(AbstractFactory):
        @staticmethod
        def create(q_object: "Q") -> "FileCount":
            print("ran factories/file_count.py create")
            subject = FileCount(q_object.query)
            return subject
