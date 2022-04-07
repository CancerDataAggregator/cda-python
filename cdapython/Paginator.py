from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cdapython.Result import Result


class Paginator:
    def __init__(self, result: "Result", to_df: bool, format_type: str = "JSON") -> None:
        self.result = result
        self.to_df = to_df
        self.count = 0
        self.stopped = False
        self.format_type = format_type

    def __iter__(self):
        return self

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
