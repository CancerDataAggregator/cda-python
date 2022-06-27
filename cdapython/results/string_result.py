from multiprocessing.pool import ApplyResult
from time import sleep
from typing import Optional

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData

from cdapython.results.result import Result


class StringResult(Result):
    def __init__(
        self,
        api_response: QueryResponseData,
        query_id: str,
        offset: Optional[int],
        limit: Optional[int],
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        format_type: str = "json",
    ) -> None:
        super().__init__(
            api_response,
            query_id,
            offset,
            limit,
            api_instance,
            show_sql,
            show_count,
            format_type,
        )

    def to_list(self, filters: Optional[str] = None) -> list:
        if filters is not None:
            values = [list(i.values())[0] for i in self._api_response.result]
            values = list(filter(None, values))
            return list(
                filter(
                    lambda items: (str(items).lower().find(str(filters)) != -1), values
                )
            )
        return [list(i.values())[0] for i in self._api_response.result]


def get_query_string_result(
    api_instance: QueryApi,
    query_id: str,
    offset: Optional[int],
    limit: Optional[int],
    async_req: Optional[bool],
    pre_stream: bool = True,
    show_sql: bool = False,
    show_count: bool = True,
    format_type: str = "json",
) -> Optional[StringResult]:
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
            return StringResult(
                response,
                query_id,
                offset,
                limit,
                api_instance,
                show_sql,
                show_count,
                format_type,
            )
