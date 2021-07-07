import Result

def get_query_result(api_instance, query_id, offset, limit):
    while True:
        response = api_instance.query(id=query_id, offset=offset, limit=limit)
        if response.total_row_count is not None:
            return Result(response, query_id, offset, limit, api_instance)