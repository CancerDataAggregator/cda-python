from typing import Tuple, Union
from cda_client import ApiClient, Configuration
from cda_client.api.query_api import QueryApi
from cda_client.model.query import Query
from constantVariables import CDA_API_URL, table_version
from Result import get_query_result
from functions import Quoted, Unquoted, col


class Q:
    """
    Q lang is Language used to send query to the cda servi
    """
    def __init__(self, *args: Tuple[str]) -> None:
        self.query = Query()

        if len(args) == 1:

            _l,  _op, _r = args[0].split(" ", 2)
            _l = col(_l)
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

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    @staticmethod
    def sql(sql: str, host: str = CDA_API_URL, dry_run: bool = False, offset: int = 0, limit: int = 1000):
        with ApiClient(
            configuration= Configuration(host=host)
        ) as api_client:
            api_instance = QueryApi(api_client)
            api_response = api_instance.sql_query(sql)
        if dry_run is True:
            return api_response
        return get_query_result(api_instance, api_response.query_id, offset, limit)

    def run(self, offset=0, limit=1000, version=table_version, host=CDA_API_URL, dry_run=False):
        """[summary]

        Args:
            offset (int, optional): [description]. Defaults to 0.
            limit (int, optional): [description]. Defaults to 1000.
            version ([type], optional): [description]. Defaults to table_version.
            host ([type], optional): [description]. Defaults to CDA_API_URL.
            dry_run (bool, optional): [description]. Defaults to False.

        Returns:
            [Result]: [description]
        """
        with ApiClient(
                configuration=Configuration(host=host)
        ) as api_client:
            api_instance = QueryApi(api_client)
            # Execute boolean query
            api_response = api_instance.boolean_query(self.query, version=version, dry_run=dry_run)
            if dry_run is True:
                return api_response
            return get_query_result(api_instance, api_response.query_id, offset, limit)

    def And(self, right: "Q"):
        return Q(self.query, "AND", right.query)

    def Or(self, right: "Q"):
        return Q(self.query, "OR", right.query)

    def From(self, right: "Q"):
        return Q(self.query, "SUBQUERY", right.query)

    def Not(self):
        return Q(self.query, "NOT", None)


def infer_quote(val: Union[int, float, str, "Q", Query]) -> Query:
    """[summary]
    Handles Strings With quotes
    Args:
        val (Union[int, float, str,): [description]

    Returns:
        Query: [description]
    """
    if isinstance(val, (Q, Query)):
        return val
    if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
        return Quoted(val[1:-1])
    return Unquoted(val)