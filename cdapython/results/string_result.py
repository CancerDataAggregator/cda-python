"""
This class inheritance from the result class it is made for unique terms function
in the utility class,just to add a different to to_list
"""
from typing import List, Optional, Any

from cda_client.api.query_api import QueryApi
from cda_client.model.query_response_data import QueryResponseData

from cdapython.results.result import Result


class StringResult(Result):
    """
    This class inheritance from the result class it is made for unique terms function
    in the utility class,just to add a different to to_list
    """

    def __init__(
        self,
        api_response: QueryResponseData,
        query_id: str,
        offset: int,
        limit: int,
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
    ) -> List[Any]:
        """_summary_
        this overloads the base Result to_list function
        Args:
            allow_substring (bool, optional): Whether the seach_value should match if it is only part of a word. Defaults to True.
            search_fields (Union[str, List[str], None]): _description_. Defaults to None.
            search_value (Optional[str], optional): _description_. Defaults to None.

        Returns:
            List[Any]: _description_
        """
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
