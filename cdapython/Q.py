from json import loads
from logging import error as logError
import logging
from multiprocessing.pool import ApplyResult
from typing import Optional, List
from urllib3.exceptions import InsecureRequestWarning, SSLError
from cdapython.ConvertionMap import convertionMap
from cdapython.Result import Result, get_query_result
from cdapython.functions import backwardsComp, col, quoted, unquoted
from cda_client.api.meta_api import MetaApi
from cdapython.decorators import measure
from typing import Union
import cdapython.constantVariables as const
from cda_client.exceptions import ServiceException
from cda_client.exceptions import ApiException
from cdapython.functions import find_ssl_path
from urllib3.connection import NewConnectionError
from urllib3.connectionpool import MaxRetryError
from cdapython.errorLogger import unverifiedHttp
from cda_client.model.query import Query
from cda_client.api.query_api import QueryApi
from cda_client import ApiClient, Configuration
from cda_client.model.query_created_data import QueryCreatedData
from cdapython.constantVariables import (
    table_version,
    default_table,
    project_name,
    default_file_table,
    file_table_version,
)
from time import sleep
import pandas as pd


logging.captureWarnings(InsecureRequestWarning)


def builder_api_client(host: Optional[str], verify: Optional[bool]) -> Configuration:
    if host is None:
        host = const.CDA_API_URL

    tmp_configuration: Configuration = Configuration(host=host)

    if verify is None:
        tmp_configuration.verify_ssl = find_ssl_path()

    if verify is False:
        unverifiedHttp()
        tmp_configuration.verify_ssl = False

    return tmp_configuration


def query_type_convertion(_op: str, _r: str):
    """_summary_
        This is for query type convertion
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


class Q:
    """
    Q lang is Language used to send query to the cda service
    """

    def __init__(self, *args: Union[str, Query, None]) -> None:
        """

        Args:
            *args (object):
        """
        self.query = Query()

        if len(args) == 1:

            if args[0] is None:
                raise RuntimeError("Q statement parse error")

            _l, _op, _r = str(args[0]).strip().replace("\n", "").split(" ", 2)
            _l = backwardsComp(_l)
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

    @staticmethod
    def set_host_url(url: str) -> None:
        const.CDA_API_URL = url

    @staticmethod
    def get_host_url() -> Optional[str]:
        return const.CDA_API_URL

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
    ):
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
            [Result | None]: [This will return a Result class]
        """
        cda_client_obj = ApiClient(
            configuration=builder_api_client(host=host, verify=verify), pool_threads=2
        )
        data: List[Result] = []

        try:

            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                api_response = api_instance.bulk_data(
                    table=table, version=version, async_req=async_call
                )

            if dry_run is True:
                return api_response

            if isinstance(api_response, ApplyResult):

                print("Waiting for results")
                while api_response.ready() is False:
                    api_response.wait(10000)
                api_response = api_response.get()

            r = get_query_result(
                api_instance, api_response.query_id, offset, limit, async_call
            )
            if r is None:
                return None

            count = 0

            while r.has_next_page is True:
                count += r.count
                print(
                    f"Row {count} out of {r.total_row_count} {int((count/r.total_row_count)*100)}%"
                )
                sleep(1)
                data.extend(r)
                r.next_page()
            df = pd.json_normalize(data=data)
            df.to_csv("test.tsv", "\t")
            return df
        except Exception as e:
            if len(data) > 0:
                df = pd.json_normalize(data)
                df.to_csv("error.tsv", "\t")
            print(e)

    @staticmethod
    def bigquery_status() -> str:
        """[summary]
        Uses the cda_client library's MetaClass to get status check on the cda
        BigQuery tablas
        Returns:
            str: status messages
        """
        return MetaApi().service_status()["systems"]["BigQueryStatus"]["messages"][0]

    def counts(
        self,
        host: Optional[str] = None,
        verify: Optional[bool] = None,
        offset: int = 0,
        limit: int = 100,
        version: Optional[str] = table_version,
        table: Optional[str] = default_table,
        async_call: bool = False,
        dry_run: Optional[bool] = False,
    ):
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
                show_sql=False,
                show_count=False,
            )

        except Exception as e:
            print(e)
        return None

    @staticmethod
    def query_job_status(
        id: str, host: Optional[str] = None, verify: Optional[bool] = None
    ):
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
        format: Optional[str] = "json",
    ) -> Optional[Result]:
        """

        Args:
            offset (int, optional): [description]. Defaults to 0.
            limit (int, optional): [description]. Defaults to 100.
            version (Optional[str], optional): [description]. Defaults to table_version.
            host (Optional[str], optional): [description]. Defaults to None.
            dry_run (bool, optional): [description]. Defaults to False.
            table (Optional[str], optional): [description]. Defaults to default_table.
            async_call (bool, optional): [description]. Defaults to False.
            verify (Optional[bool], optional): [description]. Defaults to None.
            verbose (Optional[bool], optional): [Turn on logs]. Defaults to True.

        Returns:
            Optional[Result]: [description]
        """
        cda_client_obj = ApiClient(
            configuration=builder_api_client(host=host, verify=verify)
        )

        if filter is not None:
            self.query = Q.__select(self, fields=filter).query

        try:
            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                # Execute boolean query
                if verbose:
                    print("Getting results from database", end="\n\n")
                api_response: Union[QueryCreatedData, ApplyResult] = api_instance.files(
                    self.query,
                    version=version,
                    dry_run=dry_run,
                    table=table,
                    async_req=async_call,
                )

                if isinstance(api_response, ApplyResult):
                    if verbose:
                        print("Waiting for results")
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
                show_count=False,
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

    @measure()
    def run(
        self,
        offset: int = 0,
        limit: int = 100,
        version: Optional[str] = table_version,
        host: Optional[str] = None,
        dry_run: bool = False,
        table: Optional[str] = default_table,
        async_call: bool = False,
        verify: Optional[bool] = None,
        verbose: Optional[bool] = True,
        filter: Optional[str] = None,
        flatten: Optional[bool] = False,
        format: Optional[str] = "json",
    ) -> Optional[Result]:
        """

        Args:
            offset (int, optional): [description]. Defaults to 0.
            limit (int, optional): [description]. Defaults to 100.
            version (Optional[str], optional): [description]. Defaults to table_version.
            host (Optional[str], optional): [description]. Defaults to None.
            dry_run (bool, optional): [description]. Defaults to False.
            table (Optional[str], optional): [description]. Defaults to default_table.
            async_call (bool, optional): [description]. Defaults to False.
            verify (Optional[bool], optional): [description]. Defaults to None.
            verbose (Optional[bool], optional): [Turn on logs]. Defaults to True.

        Returns:
            Optional[Result]: [description]
        """
        cda_client_obj = ApiClient(
            configuration=builder_api_client(host=host, verify=verify)
        )

        if filter is not None:
            self.query = Q.__select(self, fields=filter).query

        try:
            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                # Execute boolean query
                if verbose:
                    print("Getting results from database", end="\n\n")
                api_response: Union[
                    QueryCreatedData, ApplyResult
                ] = api_instance.boolean_query(
                    self.query,
                    version=version,
                    dry_run=dry_run,
                    table=table,
                    async_req=async_call,
                )

                if isinstance(api_response, ApplyResult):
                    if verbose:
                        print("Waiting for results")
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

    def Greater_Then_EQ(self, right: "Q"):
        return Q(self.query, ">=", right.query)

    def Greater_Then(self, right: "Q"):
        return Q(self.query, ">", right.query)

    def Less_Then_EQ(self, right: "Q"):
        return Q(self.query, "<=", right.query)

    def Less_Then(self, right: "Q"):
        return Q(self.query, "<", right.query)

    def __select(self, fields: str):
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


def infer_quote(val: Union[str, "Q", Query]) -> Union[Q, Query]:
    """[summary]
    Handles Strings With quotes
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
