from __future__ import annotations

from copy import copy

from cdapython.constant_variables import Constants


class Qconfig:
    def __init__(
        self,
        host: str = Constants.cda_api_url,
        table: str = Constants.default_table,
        version: str = Constants.table_version,
        show_sql: bool = False,
    ) -> None:
        self.host = host
        self.table = table
        self.version = version
        self.show_sql = show_sql

    def copy_config(self) -> Qconfig:
        return copy(self)
