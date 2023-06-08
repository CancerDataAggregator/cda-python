"""
This class inheritance from the result class it is made for unique terms function
in the utility class,just to add a different to to_list
"""
from typing import List, Optional

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
        offset: int,
        limit: int,
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        format_type: str = "json",
    ) -> None:
        super().__init__(
            api_response=api_response,
            offset=offset,
            limit=limit,
            api_instance=api_instance,
            show_sql=show_sql,
            show_count=show_count,
            format_type=format_type,
        )

    def get_all(self) -> None:
        pass

    def to_list(self, filters: Optional[str] = None, exact: bool = False) -> list:
        """_summary_
        this overloads the base Result to_list function
        Args:
            filters (Optional[str], optional): _description_. Defaults to None.
            exact (bool, optional): _description_. Defaults to False.

        Returns:
            list: _description_
        """
        if filters is not None and filters != "":
            filters = filters.replace("\n", " ").strip()
            values: List["StringResult"] = [
                list(i.values())[0]
                for i in self._api_response.result
                if list(i.values())[0] is not None
            ]
            # values = list(filter(None, values))
            if exact:
                return list(
                    filter(
                        lambda items: (str(items).lower() == filters.lower()),
                        values,
                    )
                )
            return list(
                filter(
                    lambda items: (str(items).lower().find(str(filters.lower())) != -1),
                    values,
                )
            )
        return [list(i.values())[0] for i in self._api_response.result]
