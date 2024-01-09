# Import directives copied from utils/utility.py

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

def unique_terms_new(
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
    print("ran utility.py unique_terms")
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


