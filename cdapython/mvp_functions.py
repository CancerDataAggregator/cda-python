
from cdapython.Q import Q

from cdapython.results.page_result import Paged_Result

from rich import print

def new_unique_terms(
    col_name,
    system = "",
    offset = 0,
    host = None,
    verify = None,
    async_req = True,
    show_sql = False,
    show_counts = False,
    verbose = True,
    limit = 100,
) -> Paged_Result:
    """
    Show all unique terms for a given column.
    Args:
        col_name (str): This is the default way to search for a unique term from the CDA service API.
        system (str, optional): his is an optional parameter used to filter the search values by data center, such as "GDC", "IDC", "PDC", or "CDS". Defaults to "".
        offset (int, optional): The number of entries to skip. Defaults to 0.
        host (Optional[str], optional): This is where the user can set a host for a different server. Defaults to None.
        verify (Optional[bool], optional): This will send a request to the cda server without verifying the SSL Cert Verification. Defaults to None.
        async_req (Optional[bool], optional): Execute request asynchronously. Defaults to True.
        show_sql (bool, optional): This will show the sql returned from the server. Defaults to False.
        show_counts (bool, optional): Show the number of occurrences for each value. Defaults to False.
        verbose (bool, optional): This will hide or show values that are automatic printed when Q runs. Defaults to True.
        limit (int, optional): the numbers of entries to return per page of data. Defaults to 100.

    Returns:
        Paged_Result
    """
    print("ran mvp_functions.py new_unique_terms")

    q_object = Q(col_name).unique_terms

    if system:
        q_object._set_system(system)

    return q_object.run(
        offset=offset,
        limit=limit,
        host=host,
        verify=verify,
        show_sql=show_sql,
        show_counts=show_counts,
        verbose=verbose,
        async_call=async_req,
    )


