
from cda_client import ApiClient
from cda_client.api.query_api import QueryApi

from cdapython.Q import Q

from cdapython.parsers.where_parser import where_parser

from cdapython.results.page_result import Paged_Result

from cdapython.utils.Cda_Configuration import CdaConfiguration

from multiprocessing.pool import ApplyResult

from rich import print

def new_unique_terms(
    col_name_arg,
    system_arg = '',
    offset_arg = 0,
    async_req_arg = True,
    show_sql_arg = False,
    show_counts_arg = False,
    verbose_arg = True,
    verify_arg = False,
    limit_arg = 100,
) -> Paged_Result:
    """
    Show all unique terms for a given column.
    Args:
        col_name_arg (str): This is the default way to search for a unique term from the CDA service API.
        system_arg (str, optional): his is an optional parameter used to filter the search values by data center, such as 'GDC', 'IDC', 'PDC', or 'CDS'. Defaults to ''.
        offset_arg (int, optional): The number of entries to skip. Defaults to 0.
        async_req_arg (Optional[bool], optional): Execute request asynchronously. Defaults to True.
        show_sql_arg (bool, optional): This will show the sql returned from the server. Defaults to False.
        show_counts_arg (bool, optional): Show the number of occurrences for each value. Defaults to False.
        verbose_arg (bool, optional): This will hide or show values that are automatic printed when Q runs. Defaults to True.
        verify_arg (Optional[bool], optional): This will send a request to the cda server without verifying the SSL Cert Verification. Defaults to None.
        limit_arg (int, optional): the numbers of entries to return per page of data. Defaults to 100.

    Returns:
        Paged_Result
    """
    print('ran mvp_functions.py new_unique_terms')

    host = 'http://localhost:8080/'

    col_name = col_name_arg.strip().replace( '\n', ' ' )

    parsed_query_object = where_parser( col_name )

    api_client_instance = ApiClient( configuration=CdaConfiguration( host=host, verify=verify_arg, verbose=verbose_arg ) )

    query_api_instance = QueryApi( api_client_instance )

    if verbose_arg:
        
        print( 'Fetching results from database...', end='\n\n' )

    paged_response_data_object = query_api_instance.unique_values(
        body=parsed_query_object.value,
        system=system_arg,
        count=show_counts_arg,
        async_req=async_req_arg,
        offset=offset_arg,
        limit=limit_arg,
        include_count=True
    )

    if isinstance( paged_response_data_object, ApplyResult ):
        
        if verbose_arg:
            
            print()

        while paged_response_data_object.ready() is False:
            
            paged_response_data_object.wait(10000)

        paged_response_data_object = paged_response_data_object.get()

    return Paged_Result(
        api_response=paged_response_data_object,
        offset=offset_arg,
        limit=limit_arg,
        api_instance=query_api_instance,
        show_sql=show_sql_arg,
        q_object=None,
        format_type='json'
    )

#    if system:
#        q_object._set_system(system)
#
#    return q_object.run(
#        offset=offset,
#        limit=limit,
#        host=host,
#        verify=verify,
#        show_sql=show_sql,
#        show_counts=show_counts,
#        verbose=verbose,
#        async_call=async_req,
#    )


