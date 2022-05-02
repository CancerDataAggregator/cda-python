from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from pandas import DataFrame

    from cdapython.Result import Result


class Paginator:
    def __init__(self, result: "Result", to_df: bool) -> None:
        self.result = result
        self.to_df = to_df
        self.count = 0
        self.stopped = False

    def __iter__(self) -> "Paginator":
        return self

    def __aiter__(self) -> "Paginator":
        return self

    async def __anext__(self) -> Optional[Union["DataFrame", "Result"]]:
        if self.stopped:
            raise StopAsyncIteration
        result_nx = self.result

        if self.to_df:
            result_nx = self.result.to_dataframe()

        if self.result.has_next_page:
            assert self.result.next_page() is not None
            self.result = self.result.next_page()
            return result_nx
        else:
            self.stopped = True
            return result_nx

    def __next__(self):
        if self.stopped:
            raise StopIteration
        self.count += self.result.count
        # print(
        #     f"Row {self.count} out of {self.result.total_row_count} {int((self.count/self.result.total_row_count)*100)}%"
        # )
        result_nx = self.result

        if self.to_df:
            result_nx = self.result.to_dataframe()

        if self.result.has_next_page:
            self.result = self.result.next_page()
            return result_nx
        else:
            self.stopped = True
            return result_nx
