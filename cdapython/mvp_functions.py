
from cda_client import ApiClient
from cda_client.api.query_api import QueryApi

from cdapython.parsers.where_parser import where_parser

from cdapython.results.page_result import Paged_Result

from cdapython.utils.Cda_Configuration import CdaConfiguration

from multiprocessing.pool import ApplyResult

from rich import print

def new_unique_terms(
    col_name,
    system = '',
    offset = 0,
    async_req = True,
    show_sql = False,
    show_counts = False,
    verbose = True,
    verify = False,
    limit = 100,
) -> Paged_Result:
    """
    Show all unique terms for a given column.
    Args:
        col_name (str): This is the default way to search for a unique term from the CDA service API.
        system (str, optional): his is an optional parameter used to filter the search values by data center, such as 'GDC', 'IDC', 'PDC', or 'CDS'. Defaults to ''.
        offset (int, optional): The number of entries to skip. Defaults to 0.
        async_req (Optional[bool], optional): Execute request asynchronously. Defaults to True.
        show_sql (bool, optional): This will show the sql returned from the server. Defaults to False.
        show_counts (bool, optional): Show the number of occurrences for each value. Defaults to False.
        verbose (bool, optional): This will hide or show values that are automatic printed when Q runs. Defaults to True.
        verify (Optional[bool], optional): This will send a request to the cda server without verifying the SSL Cert Verification. Defaults to None.
        limit (int, optional): the numbers of entries to return per page of data. Defaults to 100.

    Returns:
        Paged_Result
    """
    print('ran mvp_functions.py new_unique_terms')

    host = 'http://localhost:8080/'

    col_name = col_name.strip().replace( '\n', ' ' )

    parsed_query_object = where_parser( col_name )

    api_client_instance = ApiClient( configuration=CdaConfiguration( host=host, verify=verify, verbose=verbose ) )

    query_api_instance = QueryApi( api_client_instance )

    if verbose:
        
        print( 'Fetching results from database...', end='\n\n' )

    paged_response_data_object = query_api_instance.unique_values(
        body=parsed_query_object.value,
        system=system,
        count=show_counts,
        async_req=async_req,
        offset=offset,
        limit=limit,
        include_count=True
    )

    if isinstance( paged_response_data_object, ApplyResult ):
        
        if verbose:
            
            print()

        while paged_response_data_object.ready() is False:
            
            paged_response_data_object.wait(10000)

        paged_response_data_object = paged_response_data_object.get()

    return Paged_Result(
        api_response=paged_response_data_object,
        offset=offset,
        limit=limit,
        api_instance=query_api_instance,
        show_sql=show_sql,
        q_object=None,
        format_type='json'
    )


