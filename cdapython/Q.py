"""
Q this is the main file for Q lang.
this file holds the class for Q , links to the parsers
and SQL Like operators queue supports further to the bottom
"""
import logging
from json import JSONEncoder, dumps, loads
from multiprocessing.pool import ApplyResult
from pathlib import Path
from time import sleep
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, TypeVar, Union

from cda_client import ApiClient
from cda_client.api.meta_api import MetaApi
from cda_client.api.query_api import QueryApi
from cda_client.api_client import Endpoint
from cda_client.exceptions import ApiException, ServiceException
from cda_client.model.query import Query
from cda_client.model.query_created_data import QueryCreatedData
from cda_client.model.query_response_data import QueryResponseData
from pandas import DataFrame, concat, read_csv, read_fwf
from typing_extensions import Literal, Self
from urllib3.connection import NewConnectionError  # type: ignore
from urllib3.connectionpool import MaxRetryError
from urllib3.exceptions import InsecureRequestWarning, SSLError

from cdapython.constant_variables import Constants
from cdapython.decorators.measure import Measure
from cdapython.factories import (
    COUNT,
    DIAGNOSIS,
    FILE,
    MUTATIONS,
    RESEARCH_SUBJECT,
    SPECIMEN,
    SUBJECT,
    TREATMENT,
)
from cdapython.factories.q_factory import QFactory
from cdapython.results.result import Result, get_query_result
from cdapython.simple_parser import simple_parser
from cdapython.utils.Cda_Configuration import CdaConfiguration

logging.captureWarnings(InsecureRequestWarning)  # type: ignore
# constants
WAITING_TEXT: Literal["Waiting for results"] = "Waiting for results"


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

        """
        Using vars() over o.__dict__ dunder method,
        it is more pythonic because it is generally better to use a function over a magic/dunder method
        """
        tmp_dict: Dict[str, Any] = vars(o)
        if "query" in tmp_dict:
            return tmp_dict["query"]
        if "_data_store" in tmp_dict:
            return tmp_dict["_data_store"]

        return tmp_dict


class Q:
    """
    Q lang is Language used to send query to the cda service
    """

    def __init__(self, *args: Union[str, Query]) -> None:
        """

        Args:
            *args (object):
        """
        self.query: Query = Query()

        if len(args) == 1:
            if args[0] is None:
                raise RuntimeError("Q statement parse error")

            if isinstance(args[0], Query):
                self.query = args[0]
            else:
                query_parsed: Query = simple_parser(args[0].strip().replace("\n", " "))
                self.query = query_parsed

        elif len(args) != 3:
            raise RuntimeError(
                "Require one or three arguments. Please see documentation."
            )
        else:
            # this is for Q operators support

            _l: Union[Query, str] = args[0]
            _op: Union[Query, str] = args[1]
            _r: Union[Query, str] = args[2]

            self.query.node_type = _op
            self.query.l = _l  # noqa: E741
            self.query.r = _r  # noqa: E741

    def __repr__(self) -> str:
        return str(self.__class__) + ": \n" + str(self.__dict__)

    # region helper methods
    def to_json(
        self, indent: int = 4, write_file: bool = False, file_name: str = "Q_json_dump"
    ) -> str:
        """Created for the creating boolean-query for testing

        Returns:
            str: returns a json str to the user
        """
        tmp_json = dumps(self, indent=indent, cls=_QEncoder)
        if write_file:
            with open(f"{file_name}.json", "w") as f:
                f.write(tmp_json)
        return tmp_json

    def to_dict(self) -> Any:
        return self.query.to_dict()

    # endregion

    @classmethod
    def from_file(
        cls, field_to_search: str, file_to_search: str, key: Optional[str] = None
    ) -> "Q":
        """_summary_
            This function will read in a txt , csv or tsv and use the IN statement to search the file

        Args:
            field_to_search (str): cda column name
            file_to_search (str): user path to file
            key (Optional[str], optional): column name in csv or tsv not text

        Raises:
            IOError: _description_
            Exception: _description_
            Exception: _description_
            IOError: _description_

        Returns:
            Q
        """
        values_to_search: List[str] = []
        if not Path(file_to_search).resolve().is_file():
            raise IOError(f"File not found {Path(file_to_search).resolve()}")
        if Path(file_to_search).suffix != ".txt":
            if Path(file_to_search).suffix == ".csv":
                if key is None:
                    raise Exception("No Key for csv search")
                df = read_csv(file_to_search).fillna("")
                values_to_search.extend([f"{i}" for i in df[key].to_list()])
            elif Path(file_to_search).suffix == ".tsv":
                if key is None:
                    raise Exception("No Key for tsv search")
                df = read_csv(file_to_search, delimiter="\t").fillna("")
                values_to_search.extend([f"{i}" for i in df[key].to_list()])
            else:
                raise IOError(f"File Import Error only txt and csv supported")

        if Path(file_to_search).suffix == ".txt":
            df = read_fwf(file_to_search, header=None, sep="\n")
            values_to_search.extend([f"{i}" for i in df[0].to_list()])

        values_to_search_joined = ",".join(
            f'"{w}"' for w in list(set(filter(lambda i: i != "", values_to_search)))
        )
        query_value = f"{field_to_search} IN ({values_to_search_joined})"
        return cls(query_value)

    # region staticmethods

    @staticmethod
    def get_version() -> str:
        """returns the global version Q is pointing to

        Returns:
            str: returns a str of the current version
        """
        return Constants._VERSION

    @staticmethod
    def set_host_url(url: str) -> None:
        """this method will set the Global Q host url

        Args:
            url (str): param to set the global url
        """
        if len(url.strip()) > 0:
            Constants.CDA_API_URL = url
        else:
            print(f"Please enter a url")

    @staticmethod
    def get_host_url() -> str:
        """this method will get the Global Q host url

        Returns:
            str: returns a str of the current url
        """
        return Constants.CDA_API_URL

    @staticmethod
    def set_default_project_dataset(table: str) -> None:
        """_summary_

        Args:
            table (str): _description_
        """
        if len(table.strip()) > 0:
            Constants.default_table = table
        else:
            print(f"Please enter a table")

    @staticmethod
    def get_default_project_dataset() -> str:
        return Constants.default_table

    @staticmethod
    def set_table_version(table_version: str) -> None:
        if len(table_version.strip()) > 0:
            Constants.table_version = table_version
        else:
            print(f"Please enter a table version")

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
    ) -> Optional[DataFrame]:
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

        cda_client_obj: ApiClient = ApiClient(
            configuration=CdaConfiguration(host=host, verify=verify, verbose=verbose),
            pool_threads=2,
        )
        try:
            with cda_client_obj as api_client:
                api_instance: QueryApi = QueryApi(api_client)
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

            r: Union[Result, None] = get_query_result(
                Result, api_instance, api_response.query_id, offset, limit, async_call
            )
            if r is None:
                return None

            dataframe: DataFrame = DataFrame()
            df: DataFrame = DataFrame()
            for i in r.paginator(to_df=True):
                df: DataFrame = concat([dataframe, i])
            return df
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def bigquery_status(
        host: Optional[str] = None, verify: Optional[bool] = None
    ) -> Union[str, Any]:
        """[summary]
        Uses the cda_client library's MetaClass to get status check on the cda
        BigQuery tablas
        Returns:
            str: status messages
        """
        cda_client_obj: ApiClient = ApiClient(
            configuration=CdaConfiguration(host=host, verify=verify)
        )
        return str(
            MetaApi(api_client=cda_client_obj).service_status()["systems"][
                "BigQueryStatus"
            ]["messages"][0]
        )

    @staticmethod
    def query_job_status(
        query_id: str, host: Optional[str] = None, verify: Optional[bool] = None
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

        cda_client_obj: ApiClient = ApiClient(
            configuration=CdaConfiguration(host=host, verify=verify)
        )
        try:
            with cda_client_obj as api_client:
                api_instance: QueryApi = QueryApi(api_client)
                api_response = api_instance.job_status(query_id)
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

    @property
    def mutation(self) -> "Q":
        return QFactory.create_entity(MUTATIONS, self)

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
        self: "Q",
        offset: int = 0,
        limit: int = 100,
        version: Optional[str] = None,
        host: Optional[str] = None,
        dry_run: bool = False,
        table: Optional[str] = None,
        async_call: bool = False,
        verify: Optional[bool] = None,
        verbose: bool = True,
        include: Optional[str] = None,
        format_type: str = "json",
        show_sql: bool = False,
    ) -> Union[Result, QueryCreatedData, ApplyResult, None]:
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
        cda_client_obj: ApiClient = ApiClient(
            configuration=CdaConfiguration(host=host, verify=verify, verbose=verbose)
        )

        version, table = check_version_and_table(version, table)

        if include is not None:
            self.query = Q.__select(self, fields=include).query

        self._show_sql: bool = show_sql or False

        try:
            with cda_client_obj as api_client:
                api_instance: QueryApi = QueryApi(api_client)
                # Execute boolean query
                if verbose:
                    print(
                        "Getting results from database",
                        end="\n\n",
                    )

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
                show_sql=self._show_sql,
                show_count=True,
                format_type=format_type,
            )
        except ServiceException as http_error:
            if http_error.body is not None:
                print(
                    f"""
                Http Status: {http_error.status}
                Error Message: {loads(http_error.body)["message"]}
                """
                )

        except NewConnectionError:
            if verbose:
                print("Connection error")

        except SSLError as ssl_error:
            if verbose:
                print(ssl_error)

        except InsecureRequestWarning:
            if verbose:
                print(
                    "Adding certificate verification pem is strongly advised please read our https://cda.readthedocs.io/en/latest/Installation.html "
                )

        except MaxRetryError as max_retry_error:
            if verbose:
                print(
                    f"Connection error max retry limit of 3 hit please check url or local python ssl pem {max_retry_error}"
                )
        except ApiException as api_exception:
            if verbose:
                print(api_exception.body)
        except AttributeError as e:
            if verbose:
                print(e)
        except Exception as e:
            if verbose:
                print(e)

    def _Q_wrap(self, right: Union[str, "Q", None], op) -> "Q":
        if isinstance(right, str):
            right = Q(right)
        return self.__class__(self.query, op, right.query)

    def AND(self, right: Union[str, "Q"]) -> "Q":
        """Q's AND operator this will add a AND to between two Q queries

        Args:
            right (Q): _description_

        Returns:
            Q: a joined Q queries with a AND node
        """
        return self._Q_wrap(right, op="AND")

    def OR(self, right: Union[str, "Q"]) -> "Q":
        """Q's OR operator this will add a OR to between two Q queries

        Args:
            right (Q): _description_

        Returns:
            Q: a joined Q queries with a OR node
        """
        return self._Q_wrap(right, op="OR")

    def FROM(self, right: Union[str, "Q"]) -> "Q":
        """Q's FROM operator this will add a SUBQUERY to between two Q queries

        Args:
            right (Q): _description_

        Returns:
            Q: a joined Q queries with a SUBQUERY node
        """
        return self._Q_wrap(right, op="SUBQUERY")

    def NOT(self) -> "Q":
        """Q's FROM operator this will add a NOT to between a Q query and a None for Not

        Args:
            right (Q): _description_

        Returns:
            Q: Adds a NOT to a Q query
        """
        return self._Q_wrap(None, op="NOT")

    def _Not_EQ(self, right: Union[str, "Q"]) -> "Q":
        return self._Q_wrap(right, op="!=")

    def _Greater_Than_EQ(self, right: Union[str, "Q"]) -> "Q":
        return self._Q_wrap(right, op=">=")

    def _Greater_Than(self, right: Union[str, "Q"]) -> "Q":
        return self._Q_wrap(right, op=">")

    def _Less_Than_EQ(self, right: "Q") -> "Q":
        return self.__class__(self.query, "<=", right.query)

    def _Less_Than(self, right: "Q") -> "Q":
        return self.__class__(self.query, "<", right.query)

    def SELECT(self, fields: str) -> "Q":
        return self.__select(fields=fields)

    def ORDER_BY(self, fields: str) -> "Q":
        return self.__Order_By(fields=fields)

    def __Order_By(self, fields: str) -> "Q":
        """[summary]

        Args:
            fields (str): [takes in a list of order by values]

        Returns:
            [Q]: [returns a Q object]
        """
        # This lambda will strip a comma and rejoin the string
        mod_fields: str = (
            ",".join(map(lambda fields: fields.strip(","), fields.split()))
            .replace(":-1", " DESC")
            .replace(":1", " ASC")
        )
        tmp: Query = Query()
        tmp.node_type = "ORDERBYVALUES"
        tmp.value = mod_fields
        return self.__class__(tmp, "ORDERBY", self.query)

    def IS(self, fields: str) -> "Q":
        return self._Q_wrap(fields, op="IS")

    def __select(self, fields: str) -> "Q":
        """[summary]

        Args:
            fields (str): [takes in a list of select values]

        Returns:
            [Q]: [returns a Q object]
        """

        # This lambda will strip a comma and rejoin the string
        mod_fields: str = ",".join(
            map(lambda fields: fields.strip(","), fields.split())
        ).replace(":", " AS ")
        tmp: Query = Query()
        tmp.node_type = "SELECTVALUES"
        tmp.value = mod_fields
        return self.__class__(tmp, "SELECT", self.query)
