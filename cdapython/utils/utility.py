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
from cdapython.results.page_result import get_query_result
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


@lru_cache_timed(seconds=10)
def unique_terms(
    col_name: str,
    system: str = "",
    offset: int = 0,
    limit: int = 100,
    host: Optional[str] = None,
    verify: Optional[bool] = None,
    async_req: Optional[bool] = True,
    show_sql: bool = False,
    show_counts: bool = False,
    verbose: bool = True,
) -> Union[Result, StringResult, ColumnsResult, None]:
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
        host = Constants.cda_api_url

    if async_req is None:
        async_req = False
    col_name = col_name

    cda_client_obj: ApiClient = ApiClient(
        configuration=CdaConfiguration(host=host, verify=verify)
    )
    try:
        with cda_client_obj as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.unique_values(
                body=col_name,
                system=str(system),
                count=show_counts,
                async_req=async_req,
            )
        if isinstance(api_response, ApplyResult):
            api_response = api_response.get()

            # Execute query
            return StringResult(
                api_instance=api_instance,
                api_response=api_response,
                offset=offset,
                page_size=limit,
                show_sql=show_sql,
                show_count=True,
            )

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
    host: Optional[str] = None,
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
        host = Constants.cda_api_url

    if async_req is None:
        async_req = False

    cda_client_obj: ApiClient = ApiClient(
        configuration=CdaConfiguration(host=host, verify=verify, verbose=verbose)
    )

    try:
        with cda_client_obj as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.columns()
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


def get_drs_id(dri_id: str) -> str:
    """
    This method parse out a dri id
    Args:
        dri_id (str): dri_id
    Raises:
        Exception: _description_

    Returns:
        str: _description_
    """
    if dri_id.find("drs://") == -1:
        raise Exception("need drs_uri")
    return dri_id.replace("drs://", "")
