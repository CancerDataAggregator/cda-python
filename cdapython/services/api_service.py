from multiprocessing.pool import ApplyResult
from time import sleep
from typing import Optional

from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.model.query import Query

from cdapython.results.result import Result


class ApiService:
    @staticmethod
    def call_endpoint(
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool,
    ) -> Endpoint:
        """_summary_
            Call the endpoint to start the job for data collection.
        Args:
            api_instance (QueryApi): Api instance to use for the query
            query (Query): Query object that has been compiled
            version (str): Version to use for query
            dry_run (bool): Specify whether this is a dry run
            tabel (str): Table to perform the query on
            async_req (bool): Async request

        Returns:
            (Union[QueryCreatedData, ApplyResult])
        """
        return api_instance.boolean_query(
            query, version=version, dry_run=dry_run, table=table, async_req=async_req
        )

    @staticmethod
    def get_query_result(
        api_instance: QueryApi,
        query_id: str,
        offset: Optional[int],
        limit: Optional[int],
        async_req: Optional[bool],
        pre_stream: bool = True,
        show_sql: bool = True,
        show_count: bool = True,
        format_type: str = "json",
    ) -> Result:
        """[summary]
            This will call the next query and wait for the result then return a Result object to the user.
        Args:
            api_instance (QueryApi): [description]
            query_id (str): [description]
            offset (int): [description]
            limit (int): [description]
            async_req (bool): [description]
            pre_stream (bool, optional): [description]. Defaults to True.

        Returns:
            Optional[Result]: [returns a class Result Object]
        """
        while True:
            response = api_instance.query(
                id=query_id,
                offset=offset,
                limit=limit,
                async_req=async_req,
                _preload_content=pre_stream,
                _check_return_type=False,
            )

            if isinstance(response, ApplyResult):
                response = response.get()

            sleep(2.5)
            if response.total_row_count is not None:
                return Result(
                    response,
                    query_id,
                    offset,
                    limit,
                    api_instance,
                    show_sql,
                    show_count,
                    format_type,
                )
