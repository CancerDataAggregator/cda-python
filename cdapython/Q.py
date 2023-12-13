"""
Q this is the main file for Q lang.
this file holds the class for Q , links to the parsers
and SQL Like operators queue supports further to the bottom
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from json import JSONEncoder, dumps
from multiprocessing.pool import ApplyResult
from pathlib import Path
from types import MappingProxyType
from typing import (
    Any,
    Dict,
    Generator,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from cda_client import ApiClient
from cda_client.api.meta_api import MetaApi
from cda_client.api.query_api import QueryApi
from cda_client.exceptions import ApiException, ServiceException
from cda_client.model.paged_response_data import PagedResponseData
from cda_client.model.query import Query
from cda_client.model.query_response_data import QueryResponseData
from pandas import DataFrame, read_csv, read_fwf
from typing_extensions import Literal
from urllib3.connectionpool import MaxRetryError
from urllib3.exceptions import InsecureRequestWarning, NewConnectionError, SSLError

from cdapython.constant_variables import Constants
from cdapython.decorators.measure import Measure
from cdapython.exceptions.custom_exception import HTTP_ERROR_API, HTTP_ERROR_SERVICE
from cdapython.factories import (
    BOOLEAN_QUERY,
    COUNT,
    DIAGNOSIS,
    FILE,
    MUTATIONS,
    RESEARCH_SUBJECT,
    SPECIMEN,
    SUBJECT,
    TREATMENT,
    UNIQUE_TERMS,
)
from cdapython.factories.q_factory import QFactory
from cdapython.parsers.select_parser import sql_function_parser
from cdapython.parsers.where_parser import where_parser
from cdapython.results.page_result import Paged_Result, get_query_result
from cdapython.results.result import Result
from cdapython.utils.Cda_Configuration import CdaConfiguration
from cdapython.utils.Qconfig import Qconfig

logging.captureWarnings(False)
# constants
WAITING_TEXT: Literal["Waiting for results"] = "Waiting for results"


def check_version_and_table(
    version: Union[str, None], table: Union[str, None]
) -> Tuple[str, str]:
    """_summary_
        This is a help method that is used to check for None type
    Args:
        version (Union[str,None])
        table (Union[str,None])

    Returns:
        Tuple[str, str]
    """
    print("ran Q.py check_version_and_table")
    if version is None:
        version = Constants.table_version

    if table is None:
        table = Constants.default_table
    return (version, table)


class _QEncoder(JSONEncoder):
    """_QEncoder this is a a class to help with json conversion
        the standard json dump

    Args:
        json (_type_)
    """

    def default(self, o: Union[Q, "Query"]) -> Union[Any, Dict[str, Any], None]:
        """this will override the parent super class's default method

        Args:
            o (Union[&quot;Q&quot;, &quot;Query&quot;])

        Returns:
            Union[Any,dict[str, Any], None]
        """
        print("ran Q.py _QEncoder default")
        if isinstance(o, MappingProxyType):
            return None
        # Using vars() over o.__dict__ dunder method,
        # it is more pythonic because it is generally better to use
        # a function over a magic/dunder method
        tmp_dict: Dict[str, Any] = vars(o)
        if "query" in tmp_dict:
            return tmp_dict["query"]
        if "_data_store" in tmp_dict:
            return tmp_dict["_data_store"]
        return tmp_dict


@dataclass()
class DryClass:
    query_sql: str

    def __repr__(self) -> str:
        print("ran Q.py DryClass __repr__")
        return f"""
                SQL: {self.query_sql}
                """


T = TypeVar("T", bound="Q")


class Q:
    """
    Q lang is Language used to send query to the cda service
    """

    def __init__(
        self,
        *args: Union[str, Query],
        config: Optional[Qconfig] = None,
        debug: bool = False,
    ) -> None:
        print("ran Q.py Q __init__")
        """

        Args:
            *args (object):
        """
        self._config = Qconfig() if config is None else config
        self.query: Query = Query()
        self._show_sql: bool = False
        self.dry_run: bool = False
        self.raw_Q_string = ""
        self._system = ""
        self.limit = None
        self.offset = None
        self.show_counts = None
        if len(args) == 1:
            if args[0] is None:
                raise RuntimeError("Q statement parse error")

            if isinstance(args[0], Query):
                self.query = args[0]
            else:
                self.raw_Q_string = args[0]
                query_parsed: Query = where_parser(
                    args[0].strip().replace("\n", " "), debug=debug
                )
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

    def _set_system(self, system: str):
        """
        This will set the Q's class system for unique_terms
        Args:
            number (int): _description_
        Returns: None
        """
        print("ran Q.py Q _set_system")
        self._system = system

    def _get_system(self) -> str:
        """
        This will return the Q's system for unique_terms
        """
        print("ran Q.py Q _get_system")
        return self._system

    def _set_limit(self, number: int) -> None:
        """
        This will set the Q's class limit
        Args:
            number (int): _description_
        Returns None
        """
        print("ran Q.py Q _set_limit")
        self.limit = number

    def _get_limit(self) -> int:
        """
        This will return the Q's limit
        """
        print("ran Q.py Q _get_limit")
        return self.limit

    def _set_offset(self, number: int) -> None:
        """
        This will set the Q's class limit
        Args:
            number (int): _description_
        Returns None
        """
        print("ran Q.py Q _set_offset")
        self.offset = number

    def _get_offset(self) -> int:
        """
        This will return the Q's limit
        """
        print("ran Q.py Q _get_offset")
        return self.offset

    def __iter__(
        self,
    ) -> Union[Generator[Any, None, None], Iterator[Paged_Result]]:
        if isinstance(self, Q):
            print("ran Q.py Q __iter__")
            q_tmp_object: Q = Q(self.query, config=self._config)
            results = q_tmp_object.run(verify=False, async_call=True)
            if isinstance(results, Paged_Result):
                if results and hasattr(results, "paginator"):
                    if isinstance(results, ApplyResult):
                        results = results.get()
                    for result in results.paginator():
                        yield result

    def __repr__(self) -> str:
        print("ran Q.py Q __repr__")
        return str(self.__class__) + ": \n" + str(self.__dict__)

    def set_raw_string(self, text: str):
        print("ran Q.py Q set_raw_string")
        self.raw_Q_string = text

    def get_raw_string(self):
        print("ran Q.py Q get_raw_string")
        return self.raw_Q_string

    @staticmethod
    def get_version() -> str:
        """returns the global version Q is pointing to

        Returns:
            str: returns a str of the current version
        """
        print("ran Q.py Q get_version")
        return Constants.version()

    def set_version(self, table_version: str) -> Q:
        """
        This will set the table version
        Args:
            table_version (str)

        Returns:
            Q
        """
        print("ran Q.py Q set_version")
        config = self._config.copy_config()
        config.version = table_version
        return self.__class__(self.query, config=config)

    def set_host(self, host: str) -> Q:
        print("ran Q.py Q set_host")
        config = self._config.copy_config()
        config.host = host
        return self.__class__(self.query, config=config)

    def get_host(self) -> str:
        print("ran Q.py Q get_host")
        return self._config.host

    def set_project(self, project: str) -> Q:
        print("ran Q.py Q set_project")
        config = self._config.copy_config()
        config.table = project
        return self.__class__(self.query, config=config)

    def set_config(self, config: Qconfig = Qconfig()) -> Q:
        """
        This is used to set the config
        Args:
            config (Qconfig, optional). Defaults to Qconfig().

        Returns:
            Q
        """
        print("ran Q.py Q set_config")
        return self.__class__(self.query, config=config)

    def get_config(self) -> Qconfig:
        print("ran Q.py Q get_config")
        return self._config

    def get_table(self) -> str:
        print("ran Q.py Q get_table")
        return self._config.table

    def get_verbose(self) -> bool:
        print("ran Q.py Q get_verbose")
        return self._config.verbose

    def get_counts(self) -> bool:
        print("ran Q.py Q get_counts")
        return self._config.show_counts

    def set_counts(self, show_counts: bool) -> Q:
        """
        This will set the private property _verbose
        Args:
            value (bool)
        Returns:
            Q
        """
        print("ran Q.py Q set_counts")
        config = self._config.copy_config()
        config.show_counts = show_counts
        self.show_counts = show_counts
        return self.__class__(self.query, config=config)

    def set_verbose(self, value: bool) -> Q:
        """
        This will set the private property _verbose
        Args:
            value (bool)

        Returns:
            Q
        """
        print("ran Q.py Q set_verbose")
        config = self._config.copy_config()
        config.verbose = value
        return self.__class__(self.query, config=config)

    # region helper methods
    def to_json(
        self, indent: int = 4, write_file: bool = False, file_name: str = "Q_json_dump"
    ) -> str:
        """Created for the creating boolean-query for testing

        Returns:
            str: returns a json str to the user
        """
        print("ran Q.py Q to_json")
        tmp_json = dumps(self, indent=indent, cls=_QEncoder)
        if write_file:
            with open(f"{file_name}.json", "w", encoding="utf-8") as file:
                file.write(tmp_json)
        return tmp_json

    def to_dict(self) -> Any:
        """_summary_
        Returns the query properties as a dict
        Returns:
            Any
        """
        print("ran Q.py Q to_dict")
        return self.query.to_dict()

    # endregion
    @staticmethod
    def open_Q_file(file: str) -> Q:
        print("ran Q.py Q open_Q_file")
        path = Path(file)
        if path.suffix != ".Q":
            raise Exception("error reading .Q file")
        return Q(open(file=path.absolute(), mode="r", encoding="utf-8").read())

    @classmethod
    def from_file(
        cls,
        field_to_search: Union[List[str], str],
        file_to_search: str,
        key: str = "",
    ) -> Q:
        """_summary_
            This function will read in a txt ,
            csv or tsv and use the IN statement to search the file

        Args:
            field_to_search (str): cda column name
            file_to_search (str): user path to file
            key (Optional[str], optional): column name in csv or tsv not text

        Raises:
            IOError
            Exception
            Exception
            IOError

        Returns:
            Q
        """
        print("ran Q.py Q from_file")
        values_to_search: List[str] = []
        if not Path(file_to_search).resolve().is_file():
            raise OSError(f"File not found {Path(file_to_search).resolve()}")
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
                raise OSError("File Import Error only txt and csv supported")

        if Path(file_to_search).suffix == ".txt":
            df = read_fwf(file_to_search, header=None, sep="\n")
            values_to_search.extend([f"{i}" for i in df[0].to_list()])

        values_to_search_joined = ",".join(
            f'"{w}"' for w in list(set(filter(lambda i: i != "", values_to_search)))
        )
        query_value = f"{field_to_search} IN ({values_to_search_joined})"
        return cls(query_value)

    # region staticmethods

    @classmethod
    def bulk_download(
        cls,
        version: Union[str, None] = Constants.table_version,
        host: Union[str, None] = None,
        dry_run: bool = False,
        table: Union[str, None] = Constants.default_table,
        async_call: bool = False,
        verify: Union[bool, None] = None,
        offset: int = 0,
        limit: int = 100,
        verbose: Union[bool, None] = True,
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
        print("ran Q.py Q bulk_download")
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

            r = get_query_result(
                clz=cls,
                api_instance=api_instance,
                q_object=cast("Q", cls),
                offset=offset,
                limit=limit,
                async_req=async_call,
            )
            if r is None:
                return None

            if isinstance(r, Paged_Result):
                df: DataFrame = r.get_all().to_dataframe()
                return df

        except Exception as e:
            print(e)
        return None

    @staticmethod
    def bigquery_status(
        host: Union[str, None] = None, verify: Union[bool, None] = None
    ) -> Union[str, Any]:
        """[summary]
        Uses the cda_client library's MetaClass to get status check on the cda
        BigQuery tablas
        Returns:
            str: status messages
        """
        print("ran Q.py Q bigquery_status")
        cda_client_obj: ApiClient = ApiClient(
            configuration=CdaConfiguration(host=host, verify=verify)
        )
        return str(
            MetaApi(api_client=cda_client_obj).service_status()["systems"][
                "BigQueryStatus"
            ]["messages"][0]
        )

    # endregion

    @property
    def file(self) -> Q:
        """_summary_
        This is a chaining method used to get files
        Returns:
            _type_
        """
        print("ran Q.py Q file")
        return QFactory.create_entity(FILE, self)

    @property
    def count(self) -> Q:
        """_summary_
        This is a chaining method used to get counts
        Returns:
            _type_
        """
        print("ran Q.py Q count")
        return QFactory.create_entity(COUNT, self)

    @property
    def subject(self) -> Q:
        """
        This is a chaining method used to get subject
        Returns:
            Q
        """
        print("ran Q.py Q subject")
        return QFactory.create_entity(SUBJECT, self)

    @property
    def researchsubject(self) -> Q:
        """
        This is a chaining method used to get research subject
        Returns:
            Q
        """
        print("ran Q.py Q researchsubject")
        return QFactory.create_entity(RESEARCH_SUBJECT, self)

    @property
    def specimen(self) -> Q:
        """
        This is a chaining method used to get specimen
        Returns:
            Q
        """
        print("ran Q.py Q specimen")
        return QFactory.create_entity(SPECIMEN, self)

    @property
    def diagnosis(self) -> Q:
        """
        This is a chaining method used to get diagnosis
        Returns:
            Q
        """
        print("ran Q.py Q diagnosis")
        return QFactory.create_entity(DIAGNOSIS, self)

    @property
    def treatment(self) -> Q:
        print("ran Q.py Q treatment")
        return QFactory.create_entity(TREATMENT, self)

    @property
    def mutation(self) -> Q:
        print("ran Q.py Q mutation")
        return QFactory.create_entity(MUTATIONS, self)

    @property
    def unique_terms(self) -> Q:
        print("ran Q.py Q unique_terms")
        return QFactory.create_entity(UNIQUE_TERMS, self)

    @property
    def bool_query(self) -> Q:
        print("ran Q.py Q bool_query")
        return QFactory.create_entity(BOOLEAN_QUERY, self)

    def _call_endpoint(
        self,
        api_instance: QueryApi,
        dry_run: bool,
        offset: int,
        limit: int,
        async_req: bool,
        include_total_count: bool,
        show_counts: Optional[bool],
    ) -> PagedResponseData:
        """
        Call the endpoint to start the job for data collection.
        Args:
            api_instance (QueryApi): _description_
            dry_run (bool): _description_
            offset (int): _description_
            limit (int): _description_
            async_req (bool): _description_
            include_total_count (bool): _description_
            show_counts (Optional[bool]): Show the number of occurrences for each value

        Returns:
            PagedResponseData: _description_
        """
        print("ran Q.py Q _call_endpoint")
        factory = QFactory.create_entity(BOOLEAN_QUERY, self)
        return factory._call_endpoint(
            api_instance=api_instance,
            dry_run=dry_run,
            limit=limit,
            offset=offset,
            async_req=async_req,
            include_total_count=include_total_count,
            show_counts=show_counts,
        )

    def _build_result_object(
        self,
        api_response: QueryResponseData,
        offset: int,
        limit: int,
        api_instance: QueryApi,
        show_sql: bool,
        q_object: Q,
        format_type: str = "json",
    ) -> Result:
        print("ran Q.py Q _build_result_object")
        return Paged_Result(
            api_response=api_response,
            offset=offset,
            limit=limit,
            api_instance=api_instance,
            show_sql=show_sql,
            q_object=q_object,
            format_type=format_type,
        )

    @Measure(verbose=True)
    def run(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        host: Union[str, None] = None,
        dry_run: bool = False,
        table: Union[str, None] = None,
        async_call: bool = False,
        verify: Union[bool, None] = None,
        verbose: Union[bool, None] = True,
        include: Union[str, None] = None,
        format_type: str = "json",
        show_sql: bool = False,
        show_counts: Optional[bool] = None,
        include_total_count: bool = True,
    ) -> Union[DryClass, Result, Paged_Result, None]:
        """
        This will call the server to make a request return a Result like object
        Args:
            offset (int, optional) The number of entries to skip. Defaults to None.
            limit (int, optional) The numbers of entries to return per page of data. Defaults to None.
            host (Union[str, None], optional) This is where the user can set a host for a different server. Defaults to None.
            dry_run (bool, optional). Defaults to False.
            async_call (bool, optional) Execute request asynchronously. Defaults to False.
            verify (Union[bool, None] This will send a request to the cda server without verifying the SSL Cert Verification, optional). Defaults to None.
            verbose (bool, optional) This will hide or show values that are automatic printed when Q runs. Defaults to True.
            include (Union[str, None], optional). Defaults to None.
            format_type (str, optional). Defaults to "json".
            show_sql (bool, optional) This will show the sql returned from the server. Defaults to False.
            show_counts (bool, optional) Show the number of occurrences for each value. Defaults to False.
            include_total_count bool This will return add a param to the request to the server
        Returns:
            Union[QueryCreatedData, ApplyResult, Result, DryClass, None]: _description_
        """
        print("ran Q.py Q run")
        dry_run_current = False

        if host is None:
            host = self._config.host
        else:
            self._config.host = host
        if table is None:
            table = self._config.table
        else:
            self._config.table = table
        if verbose is None:
            verbose = self.get_verbose()
        else:
            self._config.verbose = verbose

        if dry_run is True:
            self.dry_run = False
            dry_run_current = True

        cda_client_obj: ApiClient = ApiClient(
            configuration=CdaConfiguration(host=host, verify=verify, verbose=verbose)
        )

        # version, table = check_version_and_table(version, table)

        if include is not None:
            self.query = Q.SELECT(self, fields=include).query

        if self.limit is not None:
            limit = self._get_limit()

        if self.offset is not None:
            offset = self._get_offset()
        if limit is not None:
            self._set_limit(number=limit)
        if limit is None:
            limit = 100
        if offset is not None:
            self._set_offset(offset)

        if offset is None:
            offset = 0

        if show_counts is not None:
            self._config.show_counts = show_counts

        if self.show_counts is not None:
            show_counts = self.get_counts()

        self._show_sql = show_sql or False

        try:
            with cda_client_obj as api_client:
                api_instance: QueryApi = QueryApi(api_client)
                # Execute boolean query
                if verbose:
                    print(
                        "Getting result(s) from database.",
                        end="\n\n",
                    )

                api_response: PagedResponseData = self._call_endpoint(
                    api_instance=api_instance,
                    dry_run=dry_run,
                    limit=limit,
                    offset=offset,
                    async_req=async_call,
                    include_total_count=include_total_count,
                    show_counts=show_counts,
                )
                if isinstance(api_response, ApplyResult):
                    if verbose:
                        print(WAITING_TEXT)
                    api_response = api_response.get()

                if dry_run_current is True:
                    # res
                    dryClass = DryClass(**api_response.to_dict())
                    return dryClass

            return self._build_result_object(
                api_response=api_response,
                offset=offset,
                limit=limit,
                api_instance=api_instance,
                show_sql=show_sql,
                q_object=self,
                format_type=format_type,
            )
        except ServiceException as http_error:
            if verbose:
                print(HTTP_ERROR_SERVICE(http_error=http_error))

        except ApiException as http_error:
            if verbose:
                print(HTTP_ERROR_API(http_error=http_error))

        except NewConnectionError:
            if verbose:
                print("Connection error")

        except SSLError as ssl_error:
            if verbose:
                print(ssl_error)

        except InsecureRequestWarning:
            if verbose:
                print(
                    """
                    Adding certificate verification pem is strongly
                    advised please read our
                    https://cda.readthedocs.io/en/latest/Installation.html"""
                )

        except MaxRetryError as max_retry_error:
            if verbose:
                print(
                    f"""Connection error max retry limit of 3 hit please check url
                    or local python ssl pem {max_retry_error}"""
                )

        except AttributeError as attributeError:
            if verbose:
                print(attributeError)

        except Exception as exception:
            if verbose:
                print(exception)
        return None

    def q_wrap(self, right: Union[str, Q, Query, None], operator: str) -> Q:
        """
        This function will create a Q object
        Args:
            right (Union[str, Q, Query, None])
            operator (str)

        Returns:
            Q
        """
        print("ran Q.py Q q_wrap")
        if isinstance(right, str):
            right = Q(right)
        if isinstance(right, Q):
            return self.__class__(
                self.query, operator, right.query, config=self._config
            )

    def AND(self, right: Union[str, Q]) -> Q:
        """Q's AND operator this will add a AND to between two Q queries

        Args:
            right (Q)

        Returns:
            Q: a joined Q queries with a AND node
        """
        print("ran Q.py Q AND")
        return self.q_wrap(right, operator="AND")

    def OR(self, right: Union[str, Q]) -> Q:
        """Q's OR operator this will add a OR to between two Q queries

        Args:
            right (Q)

        Returns:
            Q: a joined Q queries with a OR node
        """
        print("ran Q.py Q OR")
        return self.q_wrap(right, operator="OR")

    def FROM(self, right: Union[str, Q]) -> Q:
        """Q's FROM operator this will add a SUBQUERY to between two Q queries

        Args:
            right (Q)

        Returns:
            Q: a joined Q queries with a SUBQUERY node
        """
        print("ran Q.py Q FROM")
        return self.q_wrap(right, operator="SUBQUERY")

    def NOT(self) -> Q:
        """Q's FROM operator this will add a NOT to between a Q query and a None for Not

        Args:
            right (Q)

        Returns:
            Q: Adds a NOT to a Q query
        """
        print("ran Q.py Q NOT")
        return self.q_wrap(None, operator="NOT")

    def _Not_EQ(self, right: Union[str, Q]) -> Q:
        print("ran Q.py Q _Not_EQ")
        return self.q_wrap(right, operator="!=")

    def _Greater_Than_EQ(self, right: Union[str, Q]) -> Q:
        """_summary_
        This is a private method used for the parser
        Args:
            right (Union[str, Q])

        Returns:
            Q
        """
        print("ran Q.py Q _Greater_Than_EQ")
        return self.q_wrap(right, operator=">=")

    def _Greater_Than(self, right: Union[str, Q]) -> Q:
        """_summary_
        This is a private method used for the parser
        Args:
            right (Union[str, &quot;Q&quot;])

        Returns:
            Q
        """
        print("ran Q.py Q _Greater_Than")
        return self.q_wrap(right, operator=">")

    def _Less_Than_EQ(self, right: Q) -> Q:
        """_summary_
        This is a private method used for the parser
        Args:
            right (Q)

        Returns:
            Q
        """
        print("ran Q.py Q _Less_Than_EQ")
        return self.__class__(self.query, "<=", right.query, config=self._config)

    def _Less_Than(self, right: Q) -> Q:
        """_summary_
        This is a private method used for the parser
        Args:
            right (Q)

        Returns:
            Q
        """
        print("ran Q.py Q _Less_Than")
        return self.__class__(self.query, "<", right.query, config=self._config)

    def SELECT(self, fields: str) -> Q:
        """_summary_
        this will add fields to the SELECT values using the private select method
        Args:
            fields (str)

        Returns:
            Q
        """
        print("ran Q.py Q SELECT")
        return self.__select(fields=fields)

    def ORDER_BY(self, fields: str) -> Q:
        """_summary_
        This is like the ORDER_BY in sql
        Args:
            fields (str)

        Returns:
            Q
        """
        print("ran Q.py Q ORDER_BY")
        return self._order_by(fields=fields)

    def _order_by(self, fields: str) -> Q:
        """
        Private method will add DESC and ASC ordering,to build a Query node.
        Args:
            fields (str): [takes in a list of order by values]

        Returns:
            [Q]: [returns a Q object]
        """
        print("ran Q.py Q _order_by")
        # This lambda will strip a comma and rejoin the string
        mod_fields: str = (
            ",".join(map(lambda fields: fields.strip(","), fields.split()))
            .replace(":-1", " DESC")
            .replace(":1", " ASC")
        )
        tmp: Query = Query()
        tmp.node_type = "ORDERBYVALUES"
        tmp.value = mod_fields
        return self.__class__(tmp, "ORDERBY", self.query, config=self._config)

    def IS(self, fields: str) -> Q:
        """_summary_
        Q's IS operator this will IS Like the sql
        Args:
            fields (str)

        Returns:
            Q
        """
        print("ran Q.py Q IS")
        return self.q_wrap(fields, operator="IS")

    def __select(self, fields: str) -> Q:
        """[summary]

        Args:
            fields (str): [takes in a list of select values]

        Returns:
            [Q]: [returns a Q object]
        """
        print("ran Q.py Q __select")
        select_functions_parsed = sql_function_parser(fields)
        # # This lambda will strip a comma and rejoin the string
        # mod_fields: str = ",".join(
        #     map(lambda fields: fields.strip(","), fields.split())
        # ).replace(":", " AS ")
        # tmp: Query = Query()
        # tmp.node_type = "SELECTVALUES"
        return self.__class__(
            select_functions_parsed, "SELECT", self.query, config=self._config
        )

    def LIMIT(self, number: int) -> Q:
        print("ran Q.py Q LIMIT")
        self._set_limit(number)
        return self

    def OFFSET(self, number: int) -> Q:
        print("ran Q.py Q OFFSET")
        self._set_offset(number)
        return self
