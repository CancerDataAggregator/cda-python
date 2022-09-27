from __future__ import annotations

import json
import logging
from multiprocessing.pool import ApplyResult
from typing import TYPE_CHECKING, Optional, Union

from cda_client.api.query_api import QueryApi
from cda_client.api_client import ApiClient
from cda_client.configuration import Configuration
from cda_client.exceptions import ServiceException, ApiException
from pandas import DataFrame, json_normalize
from rich import print
from urllib3.exceptions import InsecureRequestWarning

from cdapython.constant_variables import Constants
from cdapython.decorators.cache import lru_cache_timed
from cdapython.error_logger import unverified_http
from cdapython.functions import backwards_comp, find_ssl_path
from cdapython.Qparser import parser
from cdapython.results.columns_result import ColumnsResult
from cdapython.results.result import get_query_result
from cdapython.results.string_result import StringResult

logging.captureWarnings(InsecureRequestWarning)


# This is added for Type Checking class to remove a circular import)
if TYPE_CHECKING:
    from cdapython.Q import Q
    from cdapython.results.string_result import StringResult

# Creating constant
if isinstance(Constants.default_table, str) and Constants.default_table is not None:
    DEFAULT_TABLE: Optional[str] = Constants.default_table

if (
    isinstance(Constants.default_file_table, str)
    and Constants.default_file_table is not None
):
    DEFAULT_TABLE_FILE: Optional[str] = Constants.default_file_table.split(".")[1]


if isinstance(Constants.CDA_API_URL, str):
    URL_TABLE: str = Constants.CDA_API_URL


def http_error_logger(http_error: ServiceException) -> None:
    (
        msg,
        status_code,
        _,
    ) = json.loads(http_error.body).values()
    print(
        f"""
            Http Status: {status_code}
            Error Message: {msg}
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
        if check_table not in [
            "cda_mvp",
            "integration",
            "dev",
            "cda_dev",
            "cda_prod",
            "cda_alpha",
            "cda_staging",
        ]:
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
    async_req: Optional[bool] = True,
    version: Optional[str] = Constants.table_version,
    files: Optional[bool] = False,
    show_sql: bool = False,
    show_counts: bool = False,
    verbose: bool = True,
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
        host = Constants.CDA_API_URL

    tmp_configuration: Configuration = Configuration(host=host)

    if verify is None:
        tmp_configuration.verify_ssl = find_ssl_path()

    if verify is False:
        if verbose:
            unverified_http()
        tmp_configuration.verify_ssl = False

    if table is None:
        table = Constants.default_table

    if async_req is None:
        async_req = False
    col_name = backwards_comp(col_name)
    version = table_white_list(table, version)

    cda_client_obj: ApiClient = ApiClient(configuration=tmp_configuration)
    try:
        with cda_client_obj as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.unique_values(
                version=version,
                body=col_name,
                system=str(system),
                table=table,
                count=show_counts,
                async_req=async_req,
            )
        if isinstance(api_response, ApplyResult):
            api_response = api_response.get()

            # Execute query
            query_result = get_query_result(
                StringResult,
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
        if verbose:
            http_error_logger(http_error)
    except ApiException as http_error:
        if verbose:
            http_error_logger(http_error)
    except Exception as e:
        if verbose:
            print(e)
    return None


@lru_cache_timed(seconds=60)
def columns(
    version: Optional[str] = None,
    host: Optional[str] = None,
    table: Optional[str] = None,
    verify: Optional[bool] = None,
    async_req: Optional[bool] = True,
    show_sql: bool = False,
    verbose: bool = True,
    description: bool = True,
):
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
        host = Constants.CDA_API_URL
    if version is None:
        version = Constants.table_version
    tmp_configuration: Configuration = Configuration(host=host)

    if verify is None:
        tmp_configuration.verify_ssl = find_ssl_path()

    if verify is False:
        if verbose:
            unverified_http()
        tmp_configuration.verify_ssl = False
    if table is None:
        table = Constants.default_table

    if async_req is None:
        async_req = False

    version = table_white_list(table, version)

    cda_client_obj: ApiClient = ApiClient(configuration=tmp_configuration)

    try:
        with cda_client_obj as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.columns(version=version, table=table)
            if isinstance(api_response, ApplyResult):
                api_response = api_response.get()

            if "result" in api_response:
                query_result: ColumnsResult = ColumnsResult(
                    show_sql=show_sql,
                    show_count=True,
                    result=api_response["result"],
                    description=description,
                )

            else:
                query_result: ColumnsResult = ColumnsResult(
                    show_sql=show_sql,
                    show_count=True,
                    result=api_response,
                    description=description,
                )
            result_value: ColumnsResult = query_result

            if query_result is None:
                result_value = None
                return None

            return result_value
    except ServiceException as http_error:
        if verbose:
            http_error_logger(http_error)
    except InsecureRequestWarning:
        pass
    except Exception as e:
        if verbose:
            print(e)
    return None
