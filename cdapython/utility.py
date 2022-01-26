import logging
from typing import TYPE_CHECKING, Any, List
import cda_client
from cda_client.api.query_api import QueryApi
from cdapython.Result import get_query_result
from cdapython.constantVariables import table_version
from cdapython.Qparser import parser
from typing import Optional
import numpy as np
import json
from cda_client.exceptions import ServiceException
import cdapython.constantVariables as const
from urllib3.exceptions import InsecureRequestWarning

from cdapython.errorLogger import unverfiedHttp
from .functions import find_ssl_path
from .decorators_cache import lru_cache_timed


logging.captureWarnings(InsecureRequestWarning)


# This is added for Type Checking classs to remove a circular import)
if TYPE_CHECKING:
    from cdapython.Q import Q


# Creating constant
if isinstance(const.default_table, str) and const.default_table is not None:
    DEFAULT_TABLE: Optional[str] = const.default_table.split(".")[1]


if isinstance(const.CDA_API_URL, str):
    URL_TABLE: str = const.CDA_API_URL


def http_error_logger(http_error: ServiceException):
    logging.error(
        f"""
            Http Status: {http_error.status}
            Error Message: {json.loads(http_error.body)["message"]}
            """
    )


def query(text: str) -> "Q":
    return parser(text)


def table_white_list(table: Optional[str], version: Optional[str]):
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
        if table not in ["cda_mvp", "integration", "dev"]:
            raise ValueError("Table not in allowlist list")

        if table == "cda_mvp" and version == "all_v1_1":
            version = "v3"
        return version


@lru_cache_timed(seconds=10)
def unique_terms(
    col_name: str,
    system: str = "",
    limit: int = 100,
    host: Optional[str] = None,
    table: Optional[str] = None,
    verify: Optional[bool] = None,
    async_req: Optional[bool] = None,
    pre_stream: bool = True,
    version: Optional[str] = table_version,
) -> Optional[List[Any]]:
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
        unverfiedHttp()
        tmp_configuration.verify_ssl = False

    if table is None and isinstance(const.default_table, str):
        table = DEFAULT_TABLE

    if async_req is None:
        async_req = False

    version = table_white_list(table, version)

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
            query_result = get_query_result(
                api_instance, api_response.query_id, 0, limit, async_req
            )

            if query_result is None:
                return None

            unique_array = np.array([list(t.values())[0] for t in query_result])
            return unique_array.tolist()
    except ServiceException as http_error:
        http_error_logger(http_error)

    except Exception as e:
        print(e)
    return None


@lru_cache_timed(seconds=60)
def columns(
    version: Optional[str] = table_version,
    host: Optional[str] = None,
    limit: int = 100,
    table: Optional[str] = None,
    verify: Optional[bool] = None,
    async_req: Optional[bool] = None,
    pre_stream: bool = True,
) -> Optional[object]:
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
        unverfiedHttp()
        tmp_configuration.verify_ssl = False
    if table is None and isinstance(const.default_table, str):
        table = DEFAULT_TABLE

    if async_req is None:
        async_req = False

    version = table_white_list(table, version)
    cda_client_obj = cda_client.ApiClient(configuration=tmp_configuration)

    try:
        with cda_client_obj as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.columns(version=version, table=table)
            query_result = get_query_result(
                api_instance, api_response.query_id, 0, limit, async_req
            )

            if query_result is None:
                return None

            column_array = np.array([list(t.values())[0] for t in query_result])
            return column_array.tolist()
    except ServiceException as http_error:
        http_error_logger(http_error)
    except InsecureRequestWarning:
        pass
    except Exception as e:
        print(e)
    return None
