from typing import Union, List

import cda_client
from cda_client.rest import ApiException

__version__ = "2021.1.27"

CDA_API_URL = "https://cda.cda-dev.broadinstitute.org"


def Col(col_name) -> cda_client.Query:
    return cda_client.Query(node_type="column", value=col_name)


def Quoted(quoted_val) -> cda_client.Query:
    return cda_client.Query(node_type="quoted", value=quoted_val)


def Unquoted(val) -> cda_client.Query:
    return cda_client.Query(node_type="unquoted", value=val)


def infer_quote(val: Union[int, float, str, "Q", cda_client.Query]) -> cda_client.Query:
    if isinstance(val, (Q, cda_client.Query)):
        return val
    elif isinstance(val, str):
        if val.startswith('"') and val.endswith('"'):
            return Quoted(val[1:-1])
        else:
            return Unquoted(val)
    else:
        return Unquoted(val)


class Q:
    def __init__(self, *args) -> None:
        self.query = cda_client.Query()

        if len(args) == 1:
            _l, _op, _r = args[0].split(" ", 2)
            _l = Col(_l)
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

    def run(self, offset=0, limit=None, version="v0", host=CDA_API_URL):
        with cda_client.ApiClient(
            configuration=cda_client.Configuration(host=host)
        ) as api_client:
            api_instance = cda_client.QueryApi(api_client)
            version = version  # str | Dataset version
            query = self.query  # Query | The boolean query
            offset = offset  # int | The number of entries to skip (optional)
            limit = limit  # int | The numbers of entries to return (optional)

            # Execute boolean query
            api_response = api_instance.boolean_query(
                version, query, offset=offset, limit=limit
            )
            return api_response

    def And(self, right: "Q"):
        return Q(self.query, "AND", right.query)

    def Or(self, right: "Q"):
        return Q(self.query, "OR", right.query)
