import logging

from typing import TYPE_CHECKING, Union
import cda_client
import sys
from cda_client.api.query_api import QueryApi
from cdapython.Result import get_query_result
from cdapython.constantVariables import table_version
from cdapython.Qparser import parser
from typing import Optional
import numpy as np
import json
from cda_client.exceptions import ServiceException
import cdapython.constantVariables as const
import os
import ssl
from urllib3.exceptions import InsecureRequestWarning

# This is added for Type Checking classs to remove a circular import)
if TYPE_CHECKING:
    from cdapython.Q import Q


# Creating constant
if isinstance(const.default_table, str):
    DEFAULT_TABLE: str = const.default_table.split(".")[1]


if isinstance(const.CDA_API_URL, str):
    URL_TABLE: str = const.CDA_API_URL


def httpErrorLogger(httpError: ServiceException):
    logging.error(
        f"""
            Http Status: {httpError.status}
            Error Message: {json.loads(httpError.body)["message"]}
            """
    )


def query(text: str) -> "Q":
    return parser(text)


def find_ssl_path() -> bool:
    print("checking")
    openssl_dir, openssl_cafile = os.path.split(
        ssl.get_default_verify_paths().openssl_cafile
    )
    print(openssl_dir, openssl_cafile)
    
    if openssl_cafile.find("pem"):
        return True
    else:
        return False


def tableWhiteList(table: Optional[str], version: Optional[str]) -> Optional[str]:
    """[summary]
    This checks the allowed list List and Throws a error if there is a table not allowed
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


def unique_terms(
    col_name: str,
    system: str = "",
    limit: int = 100,
    host: Optional[str] = None,
    table: Optional[str] = None,
):

    if host is None:
        host = const.CDA_API_URL

    if table is None:
        if isinstance(const.default_table, str):
            table = DEFAULT_TABLE

    version = tableWhiteList(table, table_version)

    try:
        with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=host)
        ) as api_client:
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
        httpErrorLogger(httpError)

    except Exception as e:
        print(e)


def columns(
    version: Optional[str] = table_version,
    host: Optional[str] = None,
    limit: int = 100,
    table: Optional[str] = DEFAULT_TABLE,
):
    version = tableWhiteList(table, version)
    tmp: cda_client.Configuration = cda_client.Configuration(host=host)
    try:
        # Execute query
        if host is None:
            host = const.CDA_API_URL
        if find_ssl_path():
            tmp.verify_ssl = True
        else:
            print(
                "Your ssl local cert verify has failed please review our readthedocs for help but you can still use the our lib"
            )
            tmp.verify_ssl = True
        tmp = tmp
        cda_ClientObj = cda_client.ApiClient(configuration=tmp)
        with cda_ClientObj as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.columns(version=version, table=table)
            query_result = get_query_result(
                api_instance, api_response.query_id, 0, limit
            )
            column_array = np.array([list(t.values())[0] for t in query_result])
            return column_array.tolist()

    except ServiceException as httpError:
        httpErrorLogger(httpError)
    except InsecureRequestWarning:
        pass
    except Exception as e:
        print(e)
