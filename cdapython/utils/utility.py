"""
This module is made for utility functions in Q 
"""
from __future__ import annotations
from cdapython.Q import Q
import logging
from multiprocessing.pool import ApplyResult
from typing import TYPE_CHECKING, Optional, Union

from cda_client.api.query_api import QueryApi
from cda_client.api_client import ApiClient
from cda_client.exceptions import ApiException, ServiceException
from rich import print
from urllib3.exceptions import InsecureRequestWarning

from cdapython.constant_variables import Constants
from cdapython.exceptions.custom_exception import HTTP_ERROR_API, HTTP_ERROR_SERVICE
from cdapython.results.columns_result import ColumnsResult
from cdapython.results.factories.collect_result import CollectResult
from cdapython.results.page_result import Paged_Result, get_query_result
from cdapython.results.string_result import StringResult
from cdapython.utils.Cda_Configuration import CdaConfiguration

logging.captureWarnings(InsecureRequestWarning)


# This is added for Type Checking class to remove a circular import)
if TYPE_CHECKING:
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
    host: Optional[str] = None,
    verify: Optional[bool] = None,
    async_req: Optional[bool] = True,
    show_sql: bool = False,
    show_counts: bool = False,
    verbose: bool = True,
    limit: int = 100,
) -> Paged_Result:
    # TODO : Should the value be changed? The "show_counts" parameter was copied from Swagger-generated code. Is this description sufficient?
    """
    Show all unique terms for a given column.
    Args:
        col_name (str): This is the default way to search for a unique term from the CDA service API.
        system (str, optional): his is an optional parameter used to filter the search values by data center, such as "GDC", "IDC", "PDC", or "CDS". Defaults to "".
        offset (int, optional): The number of entries to skip. Defaults to 0.
        host (Optional[str], optional): This is where the user can set a host for a different server. Defaults to None.
        verify (Optional[bool], optional): This will send a request to the cda server without verifying the SSL Cert Verification. Defaults to None.
        async_req (Optional[bool], optional): Execute request asynchronously. Defaults to True.
        show_sql (bool, optional): This will show the sql returned from the server. Defaults to False.
        show_counts (bool, optional): Show the number of occurrences for each value. Defaults to False.
        verbose (bool, optional): This will hide or show values that are automatic printed when Q runs. Defaults to True.
        limit (int, optional): the numbers of entries to return per page of data. Defaults to 100.

    Returns:
        Paged_Result
    """
    # cda_client_obj.select_header_content_type(["text/plain"])
    if system:
        q_object = Q(col_name).unique_terms
        q_object._set_system(system)
    else:
        q_object = Q(col_name).unique_terms
    return q_object.run(
        offset=offset,
        limit=limit,
        host=host,
        verify=verify,
        show_sql=show_sql,
        show_counts=show_counts,
        verbose=verbose,
        async_call=async_req,
    )


def columns(
    host: Optional[str] = None,
    verify: Optional[bool] = None,
    async_req: Optional[bool] = True,
    show_sql: bool = False,
    verbose: bool = True,
    description: bool = True,
) -> Optional[ColumnsResult]:
    """
    The Columns method displays all searchable columns in the CDA.
    Args:
        host (Optional[str], optional): This is where the user can set a host for a different server. Defaults to None.
        verify (Optional[bool], optional): This will send a request to the cda server without verifying the SSL Cert Verification. Defaults to None.
        async_req (Optional[bool], optional): Execute request asynchronously. Defaults to True.
        show_sql (bool, optional): This will show the sql returned from the server. Defaults to False.
        verbose (bool, optional): This will hide or show values that are automatic printed when Q runs. Defaults to True.
        description (bool, optional): This parameter will return a description from the server of the columns. Defaults to True.

    Returns:
        Optional[ColumnsResult]: _description_
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
                    result=api_response["result"],
                    description=description,
                )

            else:
                query_result: ColumnsResult = ColumnsResult(
                    show_sql=show_sql,
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
