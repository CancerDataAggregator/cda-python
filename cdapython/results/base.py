"""
This module was made as a base class for all results it will be imported into the result class
"""
import json
from collections import ChainMap
from typing import Any, AsyncGenerator, Dict, Iterator, List, Optional, Union

from pandas import DataFrame, Index, Series, json_normalize, merge
from rich.table import Table
from typing_extensions import Literal


class BaseResult:
    """_summary_
    This class will have all the core functionality
    for all results so it will not have to be re-implemented
    """

    def __init__(
        self,
        show_sql: bool,
        show_count: bool,
        result: List[Any],
        format_type: str = "json",
    ) -> None:
        self._result: List[Any] = result
        self.show_sql: Optional[bool] = show_sql
        self.show_count: Optional[bool] = show_count
        self.format_type: str = format_type
        self._df: DataFrame

    def __dict__(self) -> Dict[str, Any]:  # type: ignore
        return dict(ChainMap(*self._result))

    def __eq__(self, __other: object) -> Union[Any, Literal[False]]:
        return isinstance(__other, BaseResult) and self._result == __other._result

    def __hash__(self) -> int:
        return hash(tuple(self._result))

    def __contains__(self, value: str) -> bool:
        exist: bool = False
        for item in self._result:
            if value in item.values():
                exist = True

        return exist

    @property
    def count(self) -> int:
        """
        gets the count of the current list of results
        Returns:
            int
        """
        return len(self._result)

    def to_dataframe(
        self,
        record_path: Union[str, List[Any], None] = None,
        meta: Union[str, List[Union[str, List[str]]], None] = None,
        meta_prefix: Union[str, None] = None,
        max_level: Union[int, None] = None,
        search_fields: Union[List[str], str, None] = None,
        search_value: str = "",
    ) -> DataFrame:
        """[summary]
        Creates a pandas DataFrame for the Results

        Returns:
            DataFrame: [description]
        """

        _data_table: DataFrame = json_normalize(self._result)
        if search_fields == "":
            search_fields = None
        if search_fields is not None:
            data_frame = _data_table
            column_names = list(data_frame.columns)

            if isinstance(search_fields, str):
                search_fields = [search_fields]
            search_value = str(search_value)
            value: DataFrame = DataFrame(
                columns=column_names, index=Index([], dtype="int")
            )
            for i in search_fields:
                value = merge(
                    value,
                    data_frame[
                        data_frame[i].str.contains(search_value, case=False, na=False)
                    ],
                    how="right",
                    right_on=column_names,
                    left_on=column_names,
                )

            return value

        if self.format_type == "tsv":
            return self._df

        if record_path is None:
            return json_normalize(iter(self))

        return json_normalize(
            iter(self),
            max_level=max_level,
            record_path=record_path,
            meta=meta,
            meta_prefix=meta_prefix,
        )

    def df_to_table(
        self,
        pandas_dataframe: DataFrame = DataFrame([]),
        rich_table: Union[None, Table] = None,
        show_index: bool = True,
        index_name: Union[str, None] = None,
    ) -> Table:
        """Convert a pandas.DataFrame obj into a rich.Table obj.
        copied from
        https://gist.github.com/neelabalan/33ab34cf65b43e305c3f12ec6db05938#file-df_to_table-py
        Args:
            pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
            rich_table (Table): A rich Table that should be populated by the DataFrame values.
            show_index (bool): Add a column with a row count to the table. Defaults to True.
            index_name (str, optional): The column name to give to the index column.
        Returns:
            Table: The rich Table instance passed, populated with the DataFrame values.
        """

        if pandas_dataframe.empty:
            pandas_dataframe = self.to_dataframe()

        if rich_table is None:
            rich_table = Table(show_header=True, header_style="bold magenta")
        if show_index:
            index_name = str(index_name) if index_name else ""
            rich_table.add_column(index_name)

        for column in pandas_dataframe.columns:
            rich_table.add_column(str(column))

        for index, value_list in enumerate(pandas_dataframe.values.tolist()):
            row: List[str] = [str(index)] if show_index else []
            row.extend([str(x) for x in value_list])
            rich_table.add_row(*row)

        return rich_table

    def join_as_str(self, key: str, delimiter: str = ",") -> str:
        """
        This method is made for to search and join values by comma separated

        Args:
            key (str): The key value used to search json array.
            delimiter (str, optional): _description_. Defaults to ",".

        Raises:
            KeyError: This is raised if the user forgets to add a value to search on.
            Exception: This is a catch all for errors

        Returns:
            str: This returns a comma separated field
        """
        if key == "":
            raise KeyError("You need to add a value to join on")
        field_split: List[str] = key.split(".")

        if len(field_split) == 1:
            return delimiter.join(f'"{w}"' for w in [i[key] for i in self._result])

        def find_field(
            current_field_index: int, field_list: List[Any], data: Any
        ) -> Union[str, Any]:
            my_instance = data[field_list[current_field_index]]

            if current_field_index == len(field_list) - 1:
                return my_instance
            if isinstance(my_instance, dict):
                return find_field(current_field_index + 1, field_list, my_instance)
            if isinstance(my_instance, list):
                return delimiter.join(
                    [
                        find_field(current_field_index + 1, field_list, m)
                        for m in my_instance
                    ]
                )

            raise Exception("you messed up")

        tmp = delimiter.join(
            f'"{w}"'
            for w in [
                find_field(current_field_index=0, field_list=field_split, data=result)
                for result in self._result
            ]
        )
        return tmp

    def to_list(self) -> List[Any]:
        """
        This Returns a list for the results

        Returns:
            list: _description_
        """

        return self._result

    def __len__(self) -> int:
        return self.count

    def __getitem__(
        self, idx: Union[int, slice]
    ) -> Union[Series, DataFrame, Any, List[Any]]:
        """
        This access values Result as a list
        Args:
            idx (Union[int, slice]): _description_

        Returns:
            Union[Series, DataFrame, Any, list]: _description_
        """
        if isinstance(self._result, DataFrame):
            return self._result.loc[idx]

        if isinstance(idx, int):
            _idx = idx
            if idx < 0:
                _idx = self.count + idx
            return self._result[_idx]
        if isinstance(idx, slice):
            # for slicing result
            start, stop, step = idx.indices(self.count)
            range_index: range = range(start, stop, step)
            return [self._result[i] for i in range_index]

    def __iter__(self) -> Iterator[Any]:
        return iter(self._result)

    def __aiter__(self) -> AsyncGenerator[Any, None]:
        async def tmp() -> AsyncGenerator[Any, None]:
            yield self._result

        return tmp()

    def pretty_print(self, idx: Optional[int] = None) -> None:
        """_summary_
        pretty_print will print out a json object if you pass a index then it will print \
        the object at that index without the index
        it will automatically print alll results in the json object
        Args:
            idx (Optional[int], optional): _description_. Defaults to None.
        """
        if idx is None:
            for i in range(self.count):
                print(json.dumps(self[i], indent=4))
        else:
            print(json.dumps(self[idx], indent=4))
