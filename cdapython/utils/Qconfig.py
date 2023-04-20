from __future__ import annotations

from copy import copy
from typing import Optional

from cdapython.constant_variables import Constants


class Qconfig:
    def __init__(
        self,
        host: Optional[str] = None,
        table: Optional[str] = None,
        version: Optional[str] = None,
        show_sql: bool = False,
    ) -> None:
        self.host = Constants.cda_api_url if host is None else host
        self.table = Constants.default_table if table is None else table
        self.version = Constants.table_version if version is None else version
        self.show_sql = show_sql

    def copy_config(self) -> Qconfig:
        return copy(self)
