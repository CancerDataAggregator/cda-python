from typing import Optional, overload

from IPython import get_ipython
from IPython.display import display, display_html
from pandas import json_normalize
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from cdapython.results.result import Result


class CountResult(Result):
    def _repr_value(
        self, show_value: Optional[bool], show_count: Optional[bool]
    ) -> str:
        """_summary_
          This function is protected. Specifies how to display the result for counts to a user. If IPython is available,
          this will show as a set of dataframes side by side. Otherwise, it will default to a dataframe per line.
        Args:
            show_value (Optional[bool]): _description_
            show_count (Optional[bool]): _description_

        Returns:
            str: _description_
        """
        result = self[0]
        html_string: str = ""
        count_string: str = ""
        console = Console()
        tables: list[Table] = []
        for key in result:
            table = Table(title=key)
            value = result[key]
            if isinstance(value, list):
                df = json_normalize(value)
                s = df.style.hide_index()
                count_string = f"{count_string}\n\n{str(df).center(20)}"
                table.add_column(key)
                table.add_column("count")

                for item in value:
                    if item[key] is None:
                        item[key] = "null"

                    table.add_row(item[key], str(item["count"]))

                headers = {
                    "selector": "th",
                    "props": "background-color: #000066; color: white; text-align: left",
                }
                columns = {
                    "selector": "td",
                    "props": "text-align:left; border-bottom: 1px solid black;",
                }
                s.set_table_styles([headers, columns])
                s.set_table_attributes("style='display:inline'")
                html_string = html_string + s._repr_html_()

            else:
                key_string = f"{key} : {value}".center(20)
                console.print(key_string)

                count_string = count_string + "\n\n" + key_string

            tables.append(table)
        if self.isnotebook():
            display_html(html_string, raw=True)
            if self.show_sql is True:
                syntax = Syntax(
                    code=self.sql,
                    lexer="SQL",
                    indent_guides=True,
                    word_wrap=True,
                )
                console.print(syntax, overflow="fold")
            return ""
        else:
            if self.show_sql is True:
                # count_string = f"{count_string}\n\n{self.sql}"
                syntax = Syntax(
                    code=self.sql,
                    lexer="SQL",
                    indent_guides=True,
                    word_wrap=True,
                )
                console.print(syntax, overflow="fold")
            for t in tables:
                console.print(t)
            return ""

    def isnotebook(self) -> bool:
        try:
            shell = get_ipython().__class__.__name__
            if shell == "ZMQInteractiveShell":
                return True  # Jupyter notebook or qtconsole
            elif shell == "TerminalInteractiveShell":
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False  # Probably standard Python interpreter
