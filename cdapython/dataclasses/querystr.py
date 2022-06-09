from dataclasses import dataclass
from typing import Any, Optional

from cda_client.model.query import Query


@dataclass
class QueryStr(Query):
    value: str
    l: Optional[Query]
    r: Optional[Query]
    node_type: str
