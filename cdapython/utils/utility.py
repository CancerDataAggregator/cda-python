from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Optional

import cda_client
from cda_client.api.query_api import QueryApi
from cda_client.exceptions import ServiceException
from rich import print
from urllib3.exceptions import InsecureRequestWarning

import cdapython.constant_variables as const
from cdapython.constant_variables import table_version
from cdapython.decorators.cache import lru_cache_timed
from cdapython.error_logger import unverified_http
from cdapython.functions import backwards_comp, find_ssl_path
from cdapython.Qparser import parser
from cdapython.results.string_result import get_query_string_result

logging.captureWarnings(InsecureRequestWarning)


# This is added for Type Checking class to remove a circular import)
if TYPE_CHECKING:
    from cdapython.Q import Q
    from cdapython.results.string_result import StringResult

# Creating constant
if isinstance(const.default_table, str) and const.default_table is not None:
    DEFAULT_TABLE: Optional[str] = const.default_table

if isinstance(const.default_file_table, str) and const.default_file_table is not None:
    DEFAULT_TABLE_FILE: Optional[str] = const.default_file_table.split(".")[1]

if isinstance(const.file_table_version, str) and const.file_table_version is not None:
    DATABASETABLE_VERSION_FOR_FILES: Optional[str] = const.file_table_version

if isinstance(const.CDA_API_URL, str):
    URL_TABLE: str = const.CDA_API_URL


def http_error_logger(http_error: ServiceException) -> None:
    logging.error(
        f"""
            Http Status: {http_error.status}
            Error Message: {json.loads(http_error.body)["message"]}
            """
    )


def query(text: str) -> "Q":
    return parser(text)


def table_white_list(table: Optional[str], version: Optional[str]) -> Optional[str]:
    """[summary]
    This checks the allowed list List and Throws a error if there is a table
    not allowed
    Args:
        table (str): [sets table from allowed list]
        version (str): [sets the version if the value if needed]

    Raises:
        ValueError: [description]

    Returns:
        str: [description]
    """
    if table is not None and version is not None:
        if table.find(".") == -1:
            raise ValueError("Table not in allowlist list")
        check_table = table.split(".")[1]
        if check_table not in ["cda_mvp", "integration", "dev", "cda_dev"]:
            raise ValueError("Table not in allowlist list")

        if check_table == "cda_mvp" and version == "all_v1_1":
            version = "v3"

        return version
    return version


@lru_cache_timed(seconds=10)
def unique_terms(
    col_name: str,
    system: str = "",
    offset: int = 0,
    limit: int = 100,
    host: Optional[str] = None,
    table: Optional[str] = None,
    verify: Optional[bool] = None,
    async_req: Optional[bool] = None,
    version: Optional[str] = table_version,
    files: Optional[bool] = False,
    show_sql: bool = False,
) -> Optional["StringResult"]:
    """[summary]

    Args:
        col_name (str): [description]
        system (str, optional): [description]. Defaults to "".
        limit (int, optional): [description]. Defaults to 100.
        host (Optional[str], optional): [description]. Defaults to None.
        table (Optional[str], optional): [description]. Defaults to None.
        verify (Optional[bool], optional): [description]. Defaults to None.
        async_req (Optional[bool], optional): [description]. Defaults to None.
        pre_stream (bool, optional): [description]. Defaults to True.

    Returns:
        Optional[List[Any]]: [description]
    """

    if host is None:
        host = const.CDA_API_URL

    tmp_configuration: cda_client.Configuration = cda_client.Configuration(host=host)

    if verify is None:
        tmp_configuration.verify_ssl = find_ssl_path()

    if verify is False:
        unverified_http()
        tmp_configuration.verify_ssl = False

    if table is None and isinstance(const.default_table, str):
        table = DEFAULT_TABLE

    if async_req is None:
        async_req = False
    col_name = backwards_comp(col_name)
    version = table_white_list(table, version)
    if files is True:
        table = DEFAULT_TABLE_FILE
        version = DATABASETABLE_VERSION_FOR_FILES
    cda_client_obj = cda_client.ApiClient(configuration=tmp_configuration)
    try:
        with cda_client_obj as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.unique_values(
                version=version,
                body=col_name,
                system=str(system),
                table=table,
            )

            # Execute query
            query_result = get_query_string_result(
                api_instance=api_instance,
                query_id=api_response.query_id,
                offset=offset,
                limit=limit,
                async_req=async_req,
                show_sql=show_sql,
                show_count=True,
            )

            if query_result is None:
                return None

            return query_result
    except ServiceException as http_error:
        http_error_logger(http_error)

    except Exception as e:
        print(e)
    return None


@lru_cache_timed(seconds=60)
def columns(
    version: Optional[str] = table_version,
    host: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    table: Optional[str] = None,
    verify: Optional[bool] = None,
    async_req: Optional[bool] = None,
    pre_stream: bool = True,
    files: Optional[bool] = False,
    async_call: bool = False,
    show_sql: bool = False,
) -> Optional["StringResult"]:
    """[summary]

    Args:
        version (Optional[str], optional): [description]. Defaults to table_version.
        host (Optional[str], optional): [description]. Defaults to None.
        limit (int, optional): [description]. Defaults to 100.
        table (Optional[str], optional): [description]. Defaults to None.
        verify (Optional[bool], optional): [description]. Defaults to None.
        async_req (Optional[bool], optional): [description]. Defaults to None.
        pre_stream (bool, optional): [description]. Defaults to True.

    Returns:
        Optional[object]: [description]
    """

    # Execute query
    if host is None:
        host = const.CDA_API_URL

    tmp_configuration: cda_client.Configuration = cda_client.Configuration(host=host)

    if verify is None:
        tmp_configuration.verify_ssl = find_ssl_path()

    if verify is False:
        unverified_http()
        tmp_configuration.verify_ssl = False
    if table is None and isinstance(const.default_table, str):
        table = DEFAULT_TABLE

    if async_req is None:
        async_req = False

    version = table_white_list(table, version)

    if files is True:
        table = DEFAULT_TABLE_FILE
        version = DATABASETABLE_VERSION_FOR_FILES

    cda_client_obj = cda_client.ApiClient(configuration=tmp_configuration)

    try:
        with cda_client_obj as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.columns(version=version, table=table)
            query_result = get_query_string_result(
                api_instance=api_instance,
                query_id=api_response.query_id,
                offset=offset,
                limit=limit,
                async_req=async_call,
                show_sql=show_sql,
                show_count=True,
            )

            if query_result is None:
                return None

            # column_array = np.array([list(t.values())[0] for t in query_result])
            return query_result
    except ServiceException as http_error:
        http_error_logger(http_error)
    except InsecureRequestWarning:
        pass
    except Exception as e:
        print(e)
    return None
