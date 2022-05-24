from pandas import DataFrame, json_normalize
from IPython.display import display, HTML, display_html
from cdapython import Q
from tests.global_settings import host
from rich.table import Table

console = Table()
q1 = Q("sex = 'male'")
r = q1.subject.count.run(host=host)
result = r[0]
html_string = ""

for key in result:
    value = result[key]
    if type(value) is list:
        df = json_normalize(value)
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
        print(f"{key}: {value}")

display_html(html_string, raw=True)
