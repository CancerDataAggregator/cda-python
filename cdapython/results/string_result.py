from multiprocessing.pool import ApplyResult
from time import sleep
from typing import List, Optional, Union

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

    def to_list(
        self,
        search_value: Optional[str] = None,
        allow_substring: bool = True, 
    ) -> list:
        if search_value is not None:
            values: list["StringResult"] = [
                list(i.values())[0]
                for i in self._api_response.result
                if list(i.values())[0] is not None
            ]

            if allow_substring:
                # concatenate all search values
                return list(
                    filter(
                        lambda term: (
                            str(term).lower().find(str(search_value.lower())) != -1
                        ),
                        values,
                    )
                )
            else:
                return list(
                     filter(
                        lambda term: (term.lower() in search_value.lower()),
                        values,
                    )
                )
        return [list(i.values())[0] for i in self._api_response.result]
