"""
This module is made for utility functions in Q 
"""
from __future__ import annotations

import logging
from multiprocessing.pool import ApplyResult
from typing import TYPE_CHECKING, Optional, Union

from cda_client.api.query_api import QueryApi
from cda_client.api_client import ApiClient
from cda_client.exceptions import ApiException, ServiceException
from rich import print
from urllib3.exceptions import InsecureRequestWarning

from cdapython.constant_variables import Constants
from cdapython.decorators.cache import lru_cache_timed
from cdapython.exceptions.custom_exception import HTTP_ERROR_API, HTTP_ERROR_SERVICE
from cdapython.results.columns_result import ColumnsResult
from cdapython.results.factories.collect_result import CollectResult
from cdapython.results.result import get_query_result
from cdapython.results.string_result import StringResult
from cdapython.utils.Cda_Configuration import CdaConfiguration

logging.captureWarnings(InsecureRequestWarning)


# This is added for Type Checking class to remove a circular import)
if TYPE_CHECKING:
    from cdapython.Q import Q
    from cdapython.results.result import Result

# Creating constant
if isinstance(Constants.default_table, str) and Constants.default_table is not None:
    DEFAULT_TABLE: Optional[str] = Constants.default_table

if (
    isinstance(Constants.default_file_table, str)
    and Constants.default_file_table is not None
):
    DEFAULT_TABLE_FILE: Optional[str] = Constants.default_file_table.split(".")[1]

    URL_TABLE: str = Constants.cda_api_url


def get_version() -> str:
    """returns the global version Q is pointing to

    Returns:
        str: returns a str of the current version
    """
    return Constants._VERSION


def set_host_url(url: str) -> None:
    """this method will set the Global Q host url

    Args:
        url (str): param to set the global url
    """
    if len(url.strip()) > 0:
        Constants.cda_api_url = url
    else:
        print("Please enter a url")


def get_host_url() -> str:
    """this method will get the Global Q host url

    Returns:
        str: returns a str of the current url
    """
    return Constants.cda_api_url


def set_default_project_dataset(table: str) -> None:
    """_summary_

    Args:
        table (str): _description_
    """
    if len(table.strip()) > 0:
        Constants.default_table = table
    else:
        print("Please enter a table")


def get_default_project_dataset() -> str:
    return Constants.default_table


def set_table_version(table_version: str) -> None:
    if len(table_version.strip()) > 0:
        Constants.table_version = table_version
    else:
        print("Please enter a table version")


def get_table_version() -> str:
    return Constants.table_version


def unique_terms(
    col_name: str,
    system: str = "",
    offset: int = 0,
    page_size: int = 100,
    host: Optional[str] = None,
    table: Optional[str] = None,
    verify: Optional[bool] = None,
    async_req: Optional[bool] = True,
    version: Optional[str] = None,
    show_sql: bool = False,
    show_counts: bool = False,
    verbose: bool = True,
    limit: Optional[int] = None,
) -> Union[Result, StringResult, ColumnsResult, None]:
    """
    Show all unique terms for a given column.
    Args:
        col_name (str): _description_
        limit (int): Deprecated. Please use page_size
        system (str, optional): _description_. Defaults to "".
        offset (int, optional): _description_. Defaults to 0.
        page_size (int, optional): _description_. Defaults to 100.
        host (Optional[str], optional): _description_. Defaults to None.
        table (Optional[str], optional): _description_. Defaults to None.
        verify (Optional[bool], optional): _description_. Defaults to None.
        async_req (Optional[bool], optional): _description_. Defaults to True.
        version (Optional[str], optional): _description_. Defaults to None.
        show_sql (bool, optional): _description_. Defaults to False.
        show_counts (bool, optional): _description_. Defaults to False.
        verbose (bool, optional): _description_. Defaults to True.

    Returns:
        Union[Result, StringResult, ColumnsResult, None]: _description_
    """
    if version is None:
        version = Constants.table_version
    if host is None:
        host = Constants.cda_api_url

    if table is None:
        table = Constants.default_table

    if async_req is None:
        async_req = False

    if limit is not None:
        page_size = limit

    cda_client_obj: ApiClient = ApiClient(
        configuration=CdaConfiguration(host=host, verify=verify)
    )
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
            query_result: Union[
                Result, StringResult, ColumnsResult, None
            ] = get_query_result(
                clz=StringResult,
                api_instance=api_instance,
                query_id=api_response.query_id,
                offset=offset,
                limit=page_size,
                async_req=async_req,
                show_sql=show_sql,
                show_count=True,
            )

            if query_result is None:
                return None

            return query_result

    except ServiceException as http_error:
        if verbose:
            print(HTTP_ERROR_SERVICE(http_error=http_error))

    except ApiException as http_error:
        if verbose:
            print(HTTP_ERROR_API(http_error=http_error))

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
) -> Optional[ColumnsResult]:
    """
    The Columns method displays all searchable columns in the CDA.
    Args:
        version (Optional[str], optional): _description_. Defaults to None.
        host (Optional[str], optional): _description_. Defaults to None.
        table (Optional[str], optional): _description_. Defaults to None.
        verify (Optional[bool], optional): _description_. Defaults to None.
        async_req (Optional[bool], optional): _description_. Defaults to True.
        show_sql (bool, optional): _description_. Defaults to False.
        verbose (bool, optional): _description_. Defaults to True.
        description (bool, optional): _description_. Defaults to True.

    Returns:
        Optional[ColumnsResult]: _description_
    """

    # Execute query
    if host is None:
        host = Constants.cda_api_url
    if version is None:
        version = Constants.table_version

    if table is None:
        table = Constants.default_table

    if async_req is None:
        async_req = False

    cda_client_obj: ApiClient = ApiClient(
        configuration=CdaConfiguration(host=host, verify=verify, verbose=verbose)
    )

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
            result_value: Optional[ColumnsResult] = query_result

            if query_result is None:
                result_value = None
                return None

            return result_value
    except ServiceException as http_error:
        if verbose:
            print(HTTP_ERROR_SERVICE(http_error=http_error))

    except ApiException as http_error:
        if verbose:
            print(HTTP_ERROR_API(http_error=http_error))

    except InsecureRequestWarning:
        pass
    except Exception as e:
        if verbose:
            print(e)
    return None
