from functools import lru_cache
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
from .functions import find_ssl_path
from .decorators_cache import lru_cache_timed

logging.captureWarnings(InsecureRequestWarning)
# This is added for Type Checking classs to remove a circular import)


if TYPE_CHECKING:
    from cdapython.Q import Q


# Creating constant
if isinstance(const.default_table, str):
    if const.default_table is not None:
        DEFAULT_TABLE: Optional[str] = const.default_table.split(".")[1]


if isinstance(const.CDA_API_URL, str):
    URL_TABLE: str = const.CDA_API_URL


def http_error_logger(httpError: ServiceException):
    logging.error(
        f"""
            Http Status: {httpError.status}
            Error Message: {json.loads(httpError.body)["message"]}
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
        if table not in ["cda_mvp", "integration"]:
            raise ValueError("Table not in allowlist list")

        if table == "cda_mvp":
            if version == "all_v1":
                version = "v3"
        return version
    return None


@lru_cache_timed(seconds=10)
def unique_terms(
    col_name: str,
    system: str = "",
    limit: int = 100,
    host: Optional[str] = None,
    table: Optional[str] = None,
    ssl_check: Optional[bool] = None,
) -> Optional[List[Any]]:
    """[summary]

    Args:
        col_name (str): [description]
        system (str, optional): [description]. Defaults to "".
        limit (int, optional): [description]. Defaults to 100.
        host (Optional[str], optional): [description]. Defaults to None.
        table (Optional[str], optional): [description]. Defaults to None.
        ssl_check (Optional[bool], optional): [description]. Defaults to None.

    Returns:
        Optional[List[Any]]: [description]
    """
    tmp_configuration: cda_client.Configuration = cda_client.Configuration(host=host)
    if host is None:
        host = const.CDA_API_URL

    if ssl_check is None:
        tmp_configuration.verify_ssl = find_ssl_path()

    if ssl_check is False:
        tmp_configuration.verify_ssl = False

    if table is None:
        if isinstance(const.default_table, str):
            table = DEFAULT_TABLE
    version = table_white_list(table, table_version)
    cda_ClientObj = cda_client.ApiClient(configuration=tmp_configuration)
    try:
        with cda_ClientObj as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.unique_values(
                version=version,
                body=col_name,
                system=str(system),
                table=table,
            )

            # Execute query
            query_result = get_query_result(
                api_instance, api_response.query_id, 0, limit
            )
            uniqueArray = np.array([list(t.values())[0] for t in query_result])
            return uniqueArray.tolist()
    except ServiceException as httpError:
        http_error_logger(httpError)

    except Exception as e:
        print(e)
    return None


@lru_cache_timed(seconds=60)
def columns(
    version: Optional[str] = table_version,
    host: Optional[str] = None,
    limit: int = 100,
    table: Optional[str] = None,
    ssl_check: Optional[bool] = None,
) -> Optional[List[Any]]:
    """[summary]

    Args:
        version (Optional[str], optional): [description]. Defaults to table_version.
        host (Optional[str], optional): [description]. Defaults to None.
        limit (int, optional): [description]. Defaults to 100.
        table (Optional[str], optional): [description]. Defaults to None.
        ssl_check (Optional[bool], optional): [description]. Defaults to None.

    Returns:
        Optional[List[Any]]: [description]
    """

    tmp_configuration: cda_client.Configuration = cda_client.Configuration(host=host)
    # Execute query
    if host is None:
        host = const.CDA_API_URL

    if ssl_check is None:
        tmp_configuration.verify_ssl = find_ssl_path()

    if ssl_check is False:
        tmp_configuration.verify_ssl = False
    if table is None:
        if isinstance(const.default_table, str):
            table = DEFAULT_TABLE

    version = table_white_list(table, version)
    cda_ClientObj = cda_client.ApiClient(configuration=tmp_configuration)

    try:
        with cda_ClientObj as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.columns(version=version, table=table)
            query_result = get_query_result(
                api_instance, api_response.query_id, 0, limit
            )
            column_array = np.array([list(t.values())[0] for t in query_result])
            return column_array.tolist()
    except ServiceException as httpError:
        http_error_logger(httpError)
    except InsecureRequestWarning:
        pass
    except Exception as e:
        print(e)
    return None
