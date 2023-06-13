from __future__ import annotations

from copy import copy
from typing import Optional, Union

from cdapython.constant_variables import Constants


class Qconfig:
    def __init__(
        self,
        host: Optional[str] = None,
        table: Optional[str] = None,
        version: Optional[str] = None,
        show_sql: bool = False,
        verbose: Optional[bool] = None,
    ) -> None:
        """
        This class is made to keep Q's configuration settings to pass on to other Q class or methods.

        Args:
            host (Optional[str], optional): _description_. Defaults to None.
            table (Optional[str], optional): _description_. Defaults to None.
            version (Optional[str], optional): _description_. Defaults to None.
            show_sql (bool, optional): _description_. Defaults to False.
            verbose (Optional[bool], optional): _description_. Defaults to None.
        """
        self.host: str = Constants.cda_api_url if host is None else host
        self.table: str = Constants.default_table if table is None else table
        self.version: str = Constants.table_version if version is None else version
        self.show_sql: bool = show_sql
        self.verbose: Union[bool, None] = verbose if verbose is None else verbose

    def copy_config(self) -> Qconfig:
        """
        This will copy the config object
        Returns:
            Qconfig: _description_
        """
        return copy(self)
