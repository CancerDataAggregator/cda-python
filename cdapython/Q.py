import json
import logging
from json import loads
from logging import error as logError
from multiprocessing.pool import ApplyResult
from types import MappingProxyType
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, overload
from typing_extensions import Literal
import pandas as pd
from cda_client import ApiClient, Configuration
from cda_client.api.meta_api import MetaApi
from cda_client.api.query_api import QueryApi
from cda_client.exceptions import ApiException, ServiceException
from cda_client.model.query import Query
from cda_client.model.query_created_data import QueryCreatedData
from rich.progress import Progress
from urllib3.connection import NewConnectionError  # type: ignore
from urllib3.connectionpool import MaxRetryError
from urllib3.exceptions import InsecureRequestWarning, SSLError

import cdapython.constantVariables as const
from cdapython.constantVariables import (
    default_file_table,
    default_table,
    file_table_version,
    project_name,
    table_version,
)
from cdapython.decorators import measure
from cdapython.errorLogger import unverified_http
from cdapython.functions import backwards_comp, col, find_ssl_path, quoted, unquoted
from cdapython.Result import Result, get_query_result
from time import sleep
import pandas as pd
from rich.progress import Progress
from rich.traceback import Traceback
from rich import print

logging.captureWarnings(InsecureRequestWarning)  # type: ignore


# constants
WAITING_TEXT = "Waiting for results"
if isinstance(const.default_file_table, str) and const.default_file_table is not None:
    DEFAULT_TABLE_FILE: Optional[str] = const.default_file_table.split(".")[1]

if isinstance(const.file_table_version, str) and const.file_table_version is not None:
    DATABASETABLE_VERSION_FOR_FILES: Optional[str] = const.file_table_version


def builder_api_client(host: Optional[str], verify: Optional[bool]) -> Configuration:
    if host is None:
        host = const.CDA_API_URL

    tmp_configuration: Configuration = Configuration(host=host)

    if verify is None:
        tmp_configuration.verify_ssl = find_ssl_path()

    if verify is False:
        unverified_http()
        tmp_configuration.verify_ssl = False

    return tmp_configuration


def query_type_convertion(
    _op: str, _r: str
) -> Union[Tuple[Literal["LIKE"], Query], Tuple[str, str]]:
    """_summary_
        This is for query type convertion in looking operator
    Args:
        _op (str): _description_
        _r (str): _description_

    Returns:
        (tuple[Literal['LIKE'], Query] | tuple[str, str])
    """
    if _r.find("%") != -1:
        tmp = Query()
        tmp.node_type = "quoted"
        tmp.value = _r
        return ("LIKE", tmp)

    if _r.find("LIKE") != -1:
        tmp = Query()
        tmp.node_type = "quoted"
        tmp.value = _r
        return ("LIKE", tmp)

    return (_op, _r)


class _QEncoder(json.JSONEncoder):
    """_QEncoder this is a a class to help with json convetion
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
            pass
        else:
            tmp_dict = o.__dict__
            if "query" in tmp_dict:
                return tmp_dict["query"]
            if "_data_store" in tmp_dict:
                return tmp_dict["_data_store"]

            return tmp_dict
        return None


class Q:
    """
    Q lang is Language used to send query to the cda service
    """

    def __init__(self, *args: Union[str, Query]) -> None:
        """

        Args:
            *args (object):
        """
        self.query = Query()

        if len(args) == 1:

            if args[0] is None:
                raise RuntimeError("Q statement parse error")

            _l, _op, _r = str(args[0]).strip().replace("\n", "").split(" ", 2)
            _l = backwards_comp(_l)
            _l = col(_l)
            _op, _r = query_type_convertion(_op, _r)
            _r = infer_quote(_r)
        elif len(args) != 3:
            raise RuntimeError(
                "Require one or three arguments. Please see documentation."
            )
        else:
            _l = infer_quote(args[0])
            _op = args[1]
            _r = infer_quote(args[2])

        self.query.node_type = _op
        self.query.l = _l
        self.query.r = _r

    def __repr__(self) -> str:
        return str(self.__class__) + ": \n" + str(self.__dict__)

    def to_json(self, indent: int = 4) -> str:
        """Created for the creating boolean-query for testing

        Returns:
            str: returns a json str to the user
        """
        return json.dumps(self, indent=indent, cls=_QEncoder)

    @staticmethod
    def set_host_url(url: str) -> None:
        const.CDA_API_URL = url

    @staticmethod
    def get_host_url() -> str:
        return const.CDA_API_URL

    @staticmethod
    def set_default_project_dataset(table: str) -> None:
        const.default_table = table

    @staticmethod
    def get_default_project_dataset() -> str:
        return const.default_table

    @staticmethod
    def set_table_version(table_version: str) -> None:
        const.table_version = table_version

    @staticmethod
    def get_table_version() -> str:
        return const.table_version

    @staticmethod
    def sql(
        sql: str,
        host: Optional[str] = None,
        dry_run: bool = False,
        offset: int = 0,
        limit: int = 100,
        async_call: bool = False,
        verify: Optional[bool] = None,
        verbose: Optional[bool] = True,
    ) -> Optional[Result]:
        """[summary]
        This function will let you write sql instead creating a Q statement
        Args:
            sql (str): [description]
            host (Optional[str], optional): [description]. Defaults to None.
            dry_run (bool, optional): [description]. Defaults to False.
            offset (int, optional): [description]. Defaults to 0.
            limit (int, optional): [description]. Defaults to 100.
            async_call (bool, optional): [description]. Defaults to False.
            verify (Optional[bool], optional): [description]. Defaults to None.
            verbose (Optional[bool], optional): [description]. Defaults to True.

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            Optional[Result]: [description]
        """

        if (
            "create table" in sql.lower()
            or "delete from" in sql.lower()
            or "drop table" in sql.lower()
            or "update" in sql.lower()
            or "alter table" in sql.lower()
        ):
            raise Exception("Those actions are not available in Q.sql")

        if project_name is not None and sql.find(project_name) == -1:
            raise Exception("Your database is outside of the project")

        cda_client_obj = ApiClient(configuration=builder_api_client(host, verify))
        try:

            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                api_response = api_instance.sql_query(sql)
            if dry_run is True:
                return api_response

            return get_query_result(
                api_instance=api_instance,
                query_id=api_response.query_id,
                offset=offset,
                limit=limit,
                async_req=async_call,
                show_sql=True,
            )

        except Exception as e:
            print(e)
        return None

    @staticmethod
    def bulk_download(
        version: Optional[str] = table_version,
        host: Optional[str] = None,
        dry_run: bool = False,
        table: Optional[str] = default_table,
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
    def bigquery_status() -> Union[str, Any]:
        """[summary]
        Uses the cda_client library's MetaClass to get status check on the cda
        BigQuery tablas
        Returns:
            str: status messages
        """
        return str(
            MetaApi().service_status()["systems"]["BigQueryStatus"]["messages"][0]
        )

    def counts(
        self,
        host: Optional[str] = None,
        verify: Optional[bool] = None,
        offset: int = 0,
        limit: int = 100,
        version: Optional[str] = file_table_version,
        table: Optional[str] = default_file_table,
        async_call: bool = False,
        dry_run: Optional[bool] = False,
        show_sql: bool = False,
    ) -> Optional[Result]:
        """_summary_

        Args:
            host (Optional[str], optional): _description_. Defaults to None.
            verify (Optional[bool], optional): _description_. Defaults to None.
            offset (int, optional): _description_. Defaults to 0.
            limit (int, optional): _description_. Defaults to 100.
            version (Optional[str], optional): _description_. Defaults to file_table_version.
            table (Optional[str], optional): _description_. Defaults to default_file_table.
            async_call (bool, optional): _description_. Defaults to False.
            dry_run (Optional[bool], optional): _description_. Defaults to False.
            show_sql (bool, optional): _description_. Defaults to False.

        Returns:
            Result or Dataframe
        """
        cda_client_obj = ApiClient(
            configuration=builder_api_client(host=host, verify=verify)
        )
        try:

            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                api_response = api_instance.global_counts(
                    self.query,
                    version=version,
                    dry_run=dry_run,
                    table=table,
                    async_req=async_call,
                )

            if dry_run is True:
                return api_response

            return get_query_result(
                api_instance=api_instance,
                query_id=api_response.query_id,
                offset=offset,
                limit=limit,
                async_req=async_call,
                show_sql=show_sql,
                show_count=False,
            )

        except Exception as e:
            print(e)
        return None

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
                print(type(api_response))
                return api_response["status"]

        except InsecureRequestWarning as e:
            print(e)
        except Exception as e:
            print(e)
        return None

    def files(
        self,
        offset: int = 0,
        limit: int = 100,
        version: Optional[str] = file_table_version,
        host: Optional[str] = None,
        dry_run: bool = False,
        table: Optional[str] = default_file_table,
        async_call: bool = False,
        verify: Optional[bool] = None,
        verbose: Optional[bool] = True,
        filter: Optional[str] = None,
        flatten: Optional[bool] = False,
        format_type: str = "json",
    ) -> Optional[Result]:
        return self.run(
            offset,
            limit,
            version,
            host,
            dry_run,
            table,
            async_call,
            verify,
            verbose,
            filter,
            flatten,
            format,
            lambda api_instance, query, version, dry_run, table, async_req: api_instance.files(
                query,
                version=version,
                dry_run=dry_run,
                table=table,
                async_req=async_req,
            ),
        )

    def subjects(
        self,
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
        format: Optional[str] = "json",
    ):
        return self.run(
            offset,
            limit,
            version,
            host,
            dry_run,
            table,
            async_call,
            verify,
            verbose,
            filter,
            flatten,
            format,
            lambda api_instance, query, version, dry_run, table, async_req: api_instance.subject_query(
                query,
                version=version,
                dry_run=dry_run,
                table=table,
                async_req=async_req,
            ),
        )

    def research_subject(
        self,
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
        format: Optional[str] = "json",
    ):
        return self.run(
            offset,
            limit,
            version,
            host,
            dry_run,
            table,
            async_call,
            verify,
            verbose,
            filter,
            flatten,
            format,
            lambda api_instance, query, version, dry_run, table, async_req: api_instance.research_subject_query(
                query,
                version=version,
                dry_run=dry_run,
                table=table,
                async_req=async_req,
            ),
        )

    def diagnosis(
        self,
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
        format: Optional[str] = "json",
    ):
        return self.run(
            offset,
            limit,
            version,
            host,
            dry_run,
            table,
            async_call,
            verify,
            verbose,
            filter,
            flatten,
            format,
            lambda api_instance, query, version, dry_run, table, async_req: api_instance.diagnosis_query(
                query,
                version=version,
                dry_run=dry_run,
                table=table,
                async_req=async_req,
            ),
        )

    def specimen(
        self,
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
        format: Optional[str] = "json",
    ):
        return self.run(
            offset,
            limit,
            version,
            host,
            dry_run,
            table,
            async_call,
            verify,
            verbose,
            filter,
            flatten,
            format,
            lambda api_instance, query, version, dry_run, table, async_req: api_instance.specimen_query(
                query,
                version=version,
                dry_run=dry_run,
                table=table,
                async_req=async_req,
            ),
        )

    def treatments(
        self,
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
        format: Optional[str] = "json",
    ):
        return self.run(
            offset,
            limit,
            version,
            host,
            dry_run,
            table,
            async_call,
            verify,
            verbose,
            filter,
            flatten,
            format,
            lambda api_instance, query, version, dry_run, table, async_req: api_instance.treatments_query(
                query,
                version=version,
                dry_run=dry_run,
                table=table,
                async_req=async_req,
            ),
        )

    def _boolean_query(api_instance, query, version, dry_run, table, async_req):
        return api_instance.boolean_query(
            query, version=version, dry_run=dry_run, table=table, async_req=async_req
        )

    @measure()
    def run(
        self,
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
        format: Optional[str] = "json",
        callback: Optional[
            Callable[
                [QueryApi, Query, str, bool, str, bool],
                Union[QueryCreatedData, ApplyResult],
            ]
        ] = _boolean_query,
    ) -> Optional[Result]:
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
        if version is None:
            version = const.table_version

        if table is None:
            table = const.default_file_table

        if filter is not None:
            self.query = Q.__select(self, fields=filter).query

        try:
            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                # Execute boolean query
                if verbose:
                    print("Getting results from database", end="\n\n")
                api_response: Union[QueryCreatedData, ApplyResult] = callback(
                    api_instance,
                    self.query,
                    version,
                    dry_run,
                    table,
                    async_call,
                )

                if isinstance(api_response, ApplyResult):
                    if verbose:
                        print(WAITING_TEXT)
                    while api_response.ready() is False:
                        api_response.wait(10000)
                    api_response = api_response.get()

                if dry_run is True:
                    return api_response

            return get_query_result(
                api_instance=api_instance,
                query_id=api_response.query_id,
                offset=offset,
                limit=limit,
                async_req=async_call,
                show_sql=True,
                show_count=True,
                format_type=format_type,
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

    def And(self, right: "Q") -> "Q":
        return Q(self.query, "AND", right.query)

    def Or(self, right: "Q") -> "Q":
        return Q(self.query, "OR", right.query)

    def From(self, right: "Q") -> "Q":
        return Q(self.query, "SUBQUERY", right.query)

    def Not(self) -> "Q":
        return Q(self.query, "NOT", None)

    def Not_EQ(self, right: "Q") -> "Q":
        return Q(self.query, "!=", right.query)

    def Greater_Than_EQ(self, right: "Q") -> "Q":
        return Q(self.query, ">=", right.query)

    def Greater_Than(self, right: "Q") -> "Q":
        return Q(self.query, ">", right.query)

    def Less_Than_EQ(self, right: "Q") -> "Q":
        return Q(self.query, "<=", right.query)

    def Less_Than(self, right: "Q") -> "Q":
        return Q(self.query, "<", right.query)

    def Select(self, fields):
        return self.__select(fields=fields)

    def Order_By(self, fields):
        pass

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
        return Q(tmp, "SELECT", self.query)


@overload
def infer_quote(val: str) -> str:
    pass


@overload
def infer_quote(val: "Q") -> "Q":
    pass


@overload
def infer_quote(val: Query) -> Query:
    pass


def infer_quote(val):
    """[summary]
    Handles Strings With quotes by checking the value type
    Args:
        val (Union[str,"Q",Query): [description]

    Returns:
        Query: [description]
    """
    if isinstance(val, (Q, Query)):
        return val
    if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
        return quoted(val[1:-1])
    return unquoted(val)
