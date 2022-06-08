from dataclasses import dataclass
from typing import Any

from cda_client.model.query import Query


@dataclass
class QueryStr(Query):
    value: str
    l: Any
    r: Any
    node_type: Any
