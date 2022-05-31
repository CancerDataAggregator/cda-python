from typing import Optional, overload

from pandas import json_normalize
from cdapython.results.Result import Result

from IPython.display import display_html, display
from IPython import get_ipython


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
        html_string = ""
        count_string = ""

        for key in result:
            value = result[key]
            if type(value) is list:
                df = json_normalize(value)
                count_string = count_string + "\n\n" + str(df)

                s = df.style.hide_index()
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
                key_string = f"{key}: {value}"
                if self.isnotebook():
                    print(key_string)
                count_string = count_string + "\n\n" + key_string
        if self.show_sql is True:
            count_string = f"{count_string}\n\n{self.sql}"
        if self.isnotebook():
            display_html(html_string, raw=True)
            return ""
        else:
            return count_string

    def isnotebook(self):
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
