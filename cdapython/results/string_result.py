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

    def to_list(self, filters: Optional[str] = None, exact: bool = False) -> list:
        if filters is not None and filters != "":

            filters: str = filters.replace("\n", " ").strip()
            values: list["StringResult"] = [
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

            else:

                return list(
                    filter(
                        lambda items: (
                            str(items).lower().find(str(filters.lower())) != -1
                        ),
                        values,
                    )
                )
        return [list(i.values())[0] for i in self._api_response.result]
