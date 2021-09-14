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

# This is added for Type Checking classs to remove a circular import)
if TYPE_CHECKING:
    from cdapython.Q import Q


def httpErrorLogger(httpError: ServiceException):
    logging.error(
        f"""
            Http Status: {httpError.status}
            Error Message: {json.loads(httpError.body)["message"]}
            """
    )


def query(text: str) -> "Q":
    return parser(text)


def unique_terms(col_name: str, system: str = "", limit: int = 1000):
    try:
        with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=const.CDA_API_URL)
        ) as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.unique_values(
                version=table_version, body=col_name, system=str(system)
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
    limit: int = 1000,
    table: str = const.default_table.split(".")[1]
):
    if table not in ["cda_mvp", "integration"]:
        raise ValueError('Table is not in white list')

    query = f"SELECT field_path FROM `gdc-bq-sample.{table}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` WHERE table_name = '{version}'"
    sys.stderr.write(f"{query}\n")
    try:
        # Execute query
        if host is None:
            host = const.CDA_API_URL
        with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=host)
        ) as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.sql_query(query)
            query_result = get_query_result(
                api_instance, api_response.query_id, 0, limit
            )
            column_array = np.array([list(t.values())[0] for t in query_result])
            return column_array.tolist()
    except ServiceException as httpError:
        httpErrorLogger(httpError)

    except Exception as e:
        print(e)
