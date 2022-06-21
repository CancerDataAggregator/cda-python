import json
import logging
from copy import copy
from json import loads
from logging import error as logError
from multiprocessing.pool import ApplyResult
from types import MappingProxyType
from typing import Any, Dict, Optional, Tuple, TypeVar, Union, overload
from typing_extensions import TypedDict
import pandas as pd
from cda_client import ApiClient, Configuration
from cda_client.api.meta_api import MetaApi
from cda_client.api.query_api import QueryApi
from cda_client.exceptions import ApiException, ServiceException
from cda_client.model.query import Query
from cda_client.model.query_created_data import QueryCreatedData
from rich import print
from rich.progress import Progress
from typing_extensions import Literal
from urllib3.connection import NewConnectionError  # type: ignore
from urllib3.connectionpool import MaxRetryError
from urllib3.exceptions import InsecureRequestWarning, SSLError

import cdapython.constant_variables as const
from cdapython.constant_variables import default_table, project_name, table_version
from cdapython.decorators.measure import Measure
from cdapython.error_logger import unverified_http
from cdapython.exceptions.custom_exception import QSQLError, WRONGDATABASEError
from cdapython.functions import find_ssl_path
from cdapython.results.result import Result, get_query_result
from cdapython.services import (
    ApiService,
    CountsApiService,
    DiagnosisCountsService,
    DiagnosisQueryService,
    FilesApiService,
    ResearchSubjectCountsService,
    ResearchSubjectFilesService,
    ResearchSubjectQueryService,
    SpecimenCountsService,
    SpecimenFilesService,
    SpecimenQueryService,
    SubjectCountsService,
    SubjectFilesService,
    SubjectQueryService,
    TreatmentCountsService,
    TreatmentQueryService,
)
from cdapython.simple_parser import simple_parser

# from cdapython.simple_parser import simple_parser

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


def check_version_and_table(
    version: Optional[str], table: Optional[str]
) -> Tuple[str, str]:

    if version is None:
        version = const.table_version

    if table is None:
        table = const.default_file_table
    return (version, table)


class _QEncoder(json.JSONEncoder):
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

# class type_dict_api_task(TypedDict,total=False):
#         "": ApiService
#         subject: SubjectQueryService
#         researchsubject: ResearchSubjectQueryService
#         specimen: SpecimenQueryService
#         file: FilesApiService
#         count: CountsApiService
#         diagnosis: DiagnosisQueryService
#         treatment: TreatmentQueryService
#         diagnosis.file: None
#         treatment.file: None
#         subject.file: SubjectFilesService
#         researchsubject.file: ResearchSubjectFilesService
#         specimen.file: SpecimenFilesService
#         researchsubject.count: ResearchSubjectCountsService
#         diagnosis.count: DiagnosisCountsService
#         subject.count: SubjectCountsService
#         specimen.count: SpecimenCountsService
#         treatment.count: TreatmentCountsService


class Q:
    """
    Q lang is Language used to send query to the cda service
    """

    entity_type = ""
    task = ""
    api_tasks = {
        "": ApiService,
        "subject": SubjectQueryService,
        "researchsubject": ResearchSubjectQueryService,
        "specimen": SpecimenQueryService,
        "file": FilesApiService,
        "count": CountsApiService,
        "diagnosis": DiagnosisQueryService,
        "treatment": TreatmentQueryService,
        "diagnosis.file": None,
        "treatment.file": None,
        "subject.file": SubjectFilesService,
        "researchsubject.file": ResearchSubjectFilesService,
        "specimen.file": SpecimenFilesService,
        "researchsubject.count": ResearchSubjectCountsService,
        "diagnosis.count": DiagnosisCountsService,
        "subject.count": SubjectCountsService,
        "specimen.count": SpecimenCountsService,
        "treatment.count": TreatmentCountsService,
    }
    api_service = api_tasks[""]

    def __init__(self: TQ, *args: Union[str, Query]) -> None:
        """

        Args:
            *args (object):
        """
        self.query = Query()

        if len(args) == 1:

            if args[0] is None:
                raise RuntimeError("Q statement parse error")
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
        return json.dumps(self, indent=indent, cls=_QEncoder)

    def _get_func(self) -> None:
        full_string = ""
        if self.entity_type != "":
            full_string = self.entity_type

        if self.task != "":
            full_string = (
                f"{full_string}.{self.task}" if full_string != "" else self.task
            )

        self.api_service = self.api_tasks[full_string]

    # endregion

    # region staticmethods
    @staticmethod
    def get_version() -> str:
        return const.VERSION

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
            raise QSQLError("Those actions are not available in Q.sql")

        if project_name is not None and sql.find(project_name) == -1:
            raise WRONGDATABASEError("Your database is outside of the project")

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
        new_q_class = copy(self)
        new_q_class.task = "file"
        return new_q_class

    @property
    def count(self) -> "Q":
        """_summary_
        this is a chaining method used to get counts
        Returns:
            _type_: _description_
        """
        new_q_class = copy(self)
        new_q_class.task = "count"
        return new_q_class

    @property
    def subject(self) -> "Q":

        new_q_class = copy(self)
        new_q_class.entity_type = "subject"
        return new_q_class

    @property
    def researchsubject(self) -> "Q":
        new_q_class = copy(self)
        new_q_class.entity_type = "researchsubject"
        return new_q_class

    @property
    def specimen(self) -> "Q":
        new_q_class = copy(self)
        new_q_class.entity_type = "specimen"
        return new_q_class

    @property
    def diagnosis(self) -> "Q":
        new_q_class = copy(self)
        new_q_class.entity_type = "diagnosis"
        return new_q_class

    @property
    def treatment(self) -> "Q":
        new_q_class = copy(self)
        new_q_class.entity_type = "treatment"
        return new_q_class

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

        self._get_func()

        if show_sql is None:
            show_sql = self.task != "counts"

        try:
            with cda_client_obj as api_client:
                api_instance = QueryApi(api_client)
                # Execute boolean query
                if verbose:
                    print("Getting results from database", end="\n\n")
                api_response: Union[
                    QueryCreatedData, ApplyResult
                ] = self.api_service.call_endpoint(
                    api_instance=api_instance,
                    query=self.query,
                    version=version,
                    dry_run=dry_run,
                    table=table,
                    async_req=async_call,
                )
                if isinstance(api_response, ApplyResult):
                    if verbose:
                        print(WAITING_TEXT)
                    api_response = api_response.get()

                if dry_run is True:
                    return api_response

            return self.api_service.get_query_result(
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
        return Q(self.query, "AND", right.query)

    def OR(self, right: "Q") -> "Q":
        return Q(self.query, "OR", right.query)

    def FROM(self, right: "Q") -> "Q":
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

    def Select(self, fields: str) -> "Q":
        return self.__select(fields=fields)

    def __Order_By(self, fields: str) -> None:
        pass

    def Is(self, fields: str) -> "Q":
        return Q(self.query, "IS", fields)

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
