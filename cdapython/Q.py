import logging
from copy import copy
from json import JSONEncoder, dumps, loads
from logging import error as logError
from multiprocessing.pool import ApplyResult
from time import sleep
from types import MappingProxyType
from typing import Any, Dict, Optional, Tuple, TypeVar, Union
import pandas as pd
from cda_client import ApiClient, Configuration
from cda_client.api.meta_api import MetaApi
from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cdapython.factories import (
    COUNT,
    DIAGNOSIS,
    FILE,
    RESEARCH_SUBJECT,
    SPECIMEN,
    SUBJECT,
    TREATMENT,
)
from cdapython.factories.q_factory import QFactory

from cdapython.results.result import Result
from cda_client.exceptions import ApiException, ServiceException
from cda_client.model.query import Query
from cda_client.model.query_created_data import QueryCreatedData
from cda_client.model.query_response_data import QueryResponseData
from rich import print
from rich.progress import Progress
from urllib3.connection import NewConnectionError  # type: ignore
from urllib3.connectionpool import MaxRetryError
from urllib3.exceptions import InsecureRequestWarning, SSLError
from cdapython.constant_variables import Constants
from cdapython.decorators.measure import Measure
from cdapython.error_logger import unverified_http
from cdapython.functions import find_ssl_path
from cdapython.results.result import Result, get_query_result
from cdapython.simple_parser import simple_parser

logging.captureWarnings(InsecureRequestWarning)  # type: ignore


# constants
WAITING_TEXT = "Waiting for results"


def builder_api_client(host: Optional[str], verify: Optional[bool]) -> Configuration:
    if host is None:
        host = Constants.CDA_API_URL

    tmp_configuration: Configuration = Configuration(host=host)

    if verify is None:
        tmp_configuration.verify_ssl = find_ssl_path()

    if verify is False:
        unverified_http()
        tmp_configuration.verify_ssl = False

    return tmp_configuration


def check_version_and_table(
    version: Optional[str], table: Optional[str]
) -> Tuple[str, str]:

    if version is None:
        version = Constants.table_version

    if table is None:
        table = Constants.default_table
    return (version, table)


class _QEncoder(JSONEncoder):
    """_QEncoder this is a a class to help with json conversion
        the standard json dump

    Args:
        json (_type_): _description_
    """

    def default(self, o: Union["Q", "Query"]) -> Union[Any, Dict[str, Any], None]:
        """this will override the parent super class's default method

        Args:
            o (Union[&quot;Q&quot;, &quot;Query&quot;]): _description_

        Returns:
            Union[Any,dict[str, Any], None]: _description_
        """

        if isinstance(o, MappingProxyType):
            return None
        else:
            tmp_dict = o.__dict__
            if "query" in tmp_dict:
                return tmp_dict["query"]
            if "_data_store" in tmp_dict:
                return tmp_dict["_data_store"]

            return tmp_dict


TQ = TypeVar("TQ", bound="Q")


class Q:
    """
    Q lang is Language used to send query to the cda service
    """

    def __init__(self: TQ, *args: Union[str, Query]) -> None:
        """

        Args:
            *args (object):
        """
        self.query = Query()

        if len(args) == 1:

            if args[0] is None:
                raise RuntimeError("Q statement parse error")

            if type(args[0]) is Query:
                self.query = args[0]
            else:
                query_parsed = simple_parser(args[0].strip().replace("\n", " "))
                self.query = query_parsed

        elif len(args) != 3:
            raise RuntimeError(
                "Require one or three arguments. Please see documentation."
            )
        else:
            """_summary_
            this is for Q operators support
            """
            _l = args[0]
            _op = args[1]
            _r = args[2]
            self.query.node_type = _op
            self.query.l = _l
            self.query.r = _r

    def __repr__(self: TQ) -> str:
        return str(self.__class__) + ": \n" + str(self.__dict__)

    # region helper methods
    def to_json(self, indent: int = 4) -> str:
        """Created for the creating boolean-query for testing

        Returns:
            str: returns a json str to the user
        """
        return dumps(self, indent=indent, cls=_QEncoder)

    # endregion

    # region staticmethods
    @staticmethod
    def get_version() -> str:
        return Constants._VERSION

    @staticmethod
    def set_host_url(url: str) -> None:
        Constants.CDA_API_URL = url

    @staticmethod
    def get_host_url() -> str:
        return Constants.CDA_API_URL

    @staticmethod
    def set_default_project_dataset(table: str) -> None:
        Constants.default_table = table

    @staticmethod
    def get_default_project_dataset() -> str:
        return Constants.default_table

    @staticmethod
    def set_table_version(table_version: str) -> None:
        Constants.table_version = table_version

    @staticmethod
    def get_table_version() -> str:
        return Constants.table_version

    @staticmethod
    def bulk_download(
        version: Optional[str] = Constants.table_version,
        host: Optional[str] = None,
        dry_run: bool = False,
        table: Optional[str] = Constants.default_table,
        async_call: bool = False,
        verify: Optional[bool] = None,
        offset: int = 0,
        limit: int = 100,
        verbose: Optional[bool] = True,
    ) -> Optional[pd.DataFrame]:
        """[summary]

        Args:
            version (Optional[str], optional): [description]. Defaults to table_version.
            host (Optional[str], optional): [description]. Defaults to None.
            dry_run (bool, optional): [description]. Defaults to False.
            table (Optional[str], optional): [description]. Defaults to default_table.
            async_call (bool, optional): [description]. Defaults to False.
            verify (Optional[bool], optional): [description]. Defaults to None.
            offset (int, optional): [description]. Defaults to 0.
            limit (int, optional): [description]. Defaults to 100.

        Returns:
            [DataFrame | None]: [This will return a Result class]
        """

        cda_client_obj = ApiClient(
            configuration=builder_api_client(host=host, verify=verify), pool_threads=2
        )
        try:

            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                api_response = api_instance.bulk_data(
                    table=table, version=version, async_req=async_call
                )

            if dry_run is True:
                return api_response

            if isinstance(api_response, ApplyResult):
                if verbose:
                    print()

                while api_response.ready() is False:
                    api_response.wait(10000)
                api_response = api_response.get()

            r = get_query_result(
                api_instance, api_response.query_id, offset, limit, async_call
            )
            if r is None:
                return None

            df = pd.DataFrame()
            with Progress() as progress:
                download_task = progress.add_task("Download", total=r.total_row_count)
                for i in r.paginator(to_df=True):
                    df = pd.concat([df, i])
                    progress.update(download_task, advance=len(i))
            return df
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def bigquery_status(host=None, verify=None) -> Union[str, Any]:
        """[summary]
        Uses the cda_client library's MetaClass to get status check on the cda
        BigQuery tablas
        Returns:
            str: status messages
        """
        cda_client_obj = ApiClient(
            configuration=builder_api_client(host=host, verify=verify)
        )
        return str(
            MetaApi(api_client=cda_client_obj).service_status()["systems"][
                "BigQueryStatus"
            ]["messages"][0]
        )

    @staticmethod
    def query_job_status(
        id: str, host: Optional[str] = None, verify: Optional[bool] = None
    ) -> Optional[Any]:
        """[summary]

        Args:
            id (str): [description]
            host (Optional[str], optional): [description].
            Defaults to None.
            verify (Optional[bool], optional):
            [description]. Defaults to None.

        Returns:
            object: [description]
        """

        cda_client_obj = ApiClient(
            configuration=builder_api_client(host=host, verify=verify)
        )
        try:
            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                api_response = api_instance.job_status(id)
                return api_response["status"]

        except InsecureRequestWarning as e:
            print(e)
        except Exception as e:
            print(e)
        return None

    # endregion

    @property
    def file(self) -> "Q":
        """_summary_
        this is a chaining method used to get files
        Returns:
            _type_: _description_
        """
        return QFactory.create_entity(FILE, self)

    @property
    def count(self) -> "Q":
        """_summary_
        this is a chaining method used to get counts
        Returns:
            _type_: _description_
        """
        return QFactory.create_entity(COUNT, self)

    @property
    def subject(self) -> "Q":
        return QFactory.create_entity(SUBJECT, self)

    @property
    def researchsubject(self) -> "Q":
        return QFactory.create_entity(RESEARCH_SUBJECT, self)

    @property
    def specimen(self) -> "Q":
        return QFactory.create_entity(SPECIMEN, self)

    @property
    def diagnosis(self) -> "Q":
        return QFactory.create_entity(DIAGNOSIS, self)

    @property
    def treatment(self) -> "Q":
        return QFactory.create_entity(TREATMENT, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        query: Query,
        version: str,
        dry_run: bool,
        table: str,
        async_req: bool,
    ) -> Endpoint:
        """_summary_
            Call the endpoint to start the job for data collection.
        Args:
            api_instance (QueryApi): Api instance to use for the query
            query (Query): Query object that has been compiled
            version (str): Version to use for query
            dry_run (bool): Specify whether this is a dry run
            tabel (str): Table to perform the query on
            async_req (bool): Async request

        Returns:
            (Union[QueryCreatedData, ApplyResult])
        """
        return api_instance.boolean_query(
            query=query,
            version=version,
            dry_run=dry_run,
            table=table,
            async_req=async_req,
        )

    def _build_result_object(
        self,
        api_response: QueryResponseData,
        query_id: str,
        offset: Optional[int],
        limit: Optional[int],
        api_instance: QueryApi,
        show_sql: bool,
        show_count: bool,
        format_type: str = "json",
    ) -> Result:
        return Result(
            api_response,
            query_id,
            offset,
            limit,
            api_instance,
            show_sql,
            show_count,
            format_type,
        )

    def __get_query_result(
        self,
        api_instance: QueryApi,
        query_id: str,
        offset: Optional[int],
        limit: Optional[int],
        async_req: Optional[bool],
        pre_stream: bool = True,
        show_sql: bool = True,
        show_count: bool = True,
        format_type: str = "json",
    ) -> Result:
        """[summary]
            This will call the next query and wait for the result then return a Result object to the user.
        Args:
            api_instance (QueryApi): [description]
            query_id (str): [description]
            offset (int): [description]
            limit (int): [description]
            async_req (bool): [description]
            pre_stream (bool, optional): [description]. Defaults to True.

        Returns:
            Optional[Result]: [returns a class Result Object]
        """
        while True:
            response = api_instance.query(
                id=query_id,
                offset=offset,
                limit=limit,
                async_req=async_req,
                _preload_content=pre_stream,
                _check_return_type=False,
            )

            if isinstance(response, ApplyResult):
                response = response.get()

            sleep(2.5)
            if response.total_row_count is not None:
                return self._build_result_object(
                    response,
                    query_id,
                    offset,
                    limit,
                    api_instance,
                    show_sql,
                    show_count,
                    format_type,
                )

    @Measure()
    def run(
        self: TQ,
        offset: int = 0,
        limit: int = 100,
        version: Optional[str] = None,
        host: Optional[str] = None,
        dry_run: bool = False,
        table: Optional[str] = None,
        async_call: bool = False,
        verify: Optional[bool] = None,
        verbose: Optional[bool] = True,
        filter: Optional[str] = None,
        flatten: Optional[bool] = False,
        format: str = "json",
        show_sql: Optional[bool] = False,
    ) -> Union[Result, QueryCreatedData, ApplyResult]:
        """_summary_

        Args:
            offset (int, optional): _description_. Defaults to 0.
            limit (int, optional): _description_. Defaults to 100.
            version (Optional[str], optional): _description_. Defaults to None.
            host (Optional[str], optional): _description_. Defaults to None.
            dry_run (bool, optional): _description_. Defaults to False.
            table (Optional[str], optional): _description_. Defaults to None.
            async_call (bool, optional): _description_. Defaults to False.
            verify (Optional[bool], optional): _description_. Defaults to None.
            verbose (Optional[bool], optional): _description_. Defaults to True.
            filter (Optional[str], optional): _description_. Defaults to None.
            flatten (Optional[bool], optional): _description_. Defaults to False.
            format (Optional[str], optional): _description_. Defaults to "json".

        Returns:
            Optional[Result]: _description_
        """

        cda_client_obj = ApiClient(
            configuration=builder_api_client(host=host, verify=verify)
        )

        version, table = check_version_and_table(version, table)

        if filter is not None:
            self.query = Q.__select(self, fields=filter).query

        if show_sql is None:
            show_sql = False

        try:
            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                # Execute boolean query
                if verbose:
                    print("Getting results from database", end="\n\n")
                api_response: Union[
                    QueryCreatedData, ApplyResult
                ] = self._call_endpoint(
                    api_instance=api_instance,
                    query=self.query,
                    version=version,
                    dry_run=dry_run,
                    table=table,
                    async_req=async_call,
                )  # type: ignore
                if isinstance(api_response, ApplyResult):
                    if verbose:
                        print(WAITING_TEXT)
                    api_response = api_response.get()

                if dry_run is True:
                    return api_response

            return self.__get_query_result(
                api_instance=api_instance,
                query_id=api_response.query_id,  # type: ignore
                offset=offset,
                limit=limit,
                async_req=async_call,
                show_sql=show_sql,
                show_count=True,
                format_type=format,
            )
        except ServiceException as httpError:
            if httpError.body is not None:
                logError(
                    f"""
                Http Status: {httpError.status}
                Error Message: {loads(httpError.body)["message"]}
                """
                )

        except NewConnectionError:
            print("Connection error")

        except SSLError as e:
            print(e)

        except InsecureRequestWarning:
            print(
                "Adding certificate verification pem is strongly advised please read our https://cda.readthedocs.io/en/latest/Installation.html "
            )

        except MaxRetryError as e:
            print(
                f"Connection error max retry limit of 3 hit please check url or local python ssl pem {e}"
            )
        except ApiException as e:
            print(e.body)

        except Exception as e:
            print(e)
        return None

    def AND(self, right: "Q") -> "Q":
        return self.__class__(self.query, "AND", right.query)

    def OR(self, right: "Q") -> "Q":
        return self.__class__(self.query, "OR", right.query)

    def FROM(self, right: "Q") -> "Q":
        return self.__class__(self.query, "SUBQUERY", right.query)

    def NOT(self) -> "Q":
        return self.__class__(self.query, "NOT", None)

    def _Not_EQ(self, right: "Q") -> "Q":
        return self.__class__(self.query, "!=", right.query)

    def _Greater_Than_EQ(self, right: "Q") -> "Q":
        return self.__class__(self.query, ">=", right.query)

    def _Greater_Than(self, right: "Q") -> "Q":
        return self.__class__(self.query, ">", right.query)

    def _Less_Than_EQ(self, right: "Q") -> "Q":
        return self.__class__(self.query, "<=", right.query)

    def _Less_Than(self, right: "Q") -> "Q":
        return self.__class__(self.query, "<", right.query)

    def SELECT(self, fields: str) -> "Q":
        return self.__select(fields=fields)

    def __Order_By(self, fields: str) -> None:
        pass

    def IS(self, fields: str) -> "Q":
        return self.__class__(self.query, "IS", fields)

    def __select(self, fields: str) -> "Q":
        """[summary]

        Args:
            fields (str): [takes in a list of select values]

        Returns:
            [Q]: [returns a Q object]
        """
        ""
        # This lambda will strip a comma and rejoin the string
        fields = ",".join(map(lambda fields: fields.strip(","), fields.split()))

        tmp = Query()
        tmp.node_type = "SELECTVALUES"
        tmp.value = fields
        return self.__class__(tmp, "SELECT", self.query)
