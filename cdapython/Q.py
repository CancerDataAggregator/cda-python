import cda_client
from cda_client.api.query_api import QueryApi
from cda_client.model.query import Query 
from constantVariables import CDA_API_URL,table_version,__version__
from .get_query_result import get_query_result
from .functions import Col
from .infer_quote import infer_quote

class Q:
    def __init__(self, *args) -> None:
        self.query = Query()

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
    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def run(self, offset=0, limit=1000, version=table_version, host=CDA_API_URL, dry_run=False):
        with cda_client.ApiClient(
                configuration=cda_client.Configuration(host=host)
        ) as api_client:
            api_instance = QueryApi(api_client)
            # Execute boolean query
            api_response = api_instance.boolean_query(self.query, version=version, dry_run=dry_run)
            if dry_run is True:
                return api_response
            return get_query_result(api_instance, api_response.query_id, offset, limit)
