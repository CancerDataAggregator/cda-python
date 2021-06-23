import pprint as pp
import get_query_result
class Result:
    """A convenient wrapper around the response object from the CDA service."""

    def __init__(self, api_response, query_id, offset, limit, api_instance) -> None:
        self._api_response = api_response
        self._query_id = query_id
        self._offset = offset
        self._limit = limit
        self._api_instance = api_instance

    def __str__(self) -> str:
        return f"""
Query: {self.sql}
Offset: {self._offset}
Count: {self.count}
Total Row Count: {self.total_row_count}
More pages: {self.has_next_page}
"""

    @property
    def sql(self):
        return self._api_response.query_sql

    @property
    def count(self):
        return len(self._api_response.result)

    @property
    def total_row_count(self):
        return self._api_response.total_row_count

    @property
    def has_next_page(self):
        return (self._offset + self._limit) <= self.total_row_count

    def __getitem__(self, idx):
        return self._api_response.result[idx]

    def pretty_print(self, idx):
        pp.pprint(self[idx])

    def next_page(self, limit=None):
        if not self.has_next_page:
            raise StopIteration

        _offset = self._offset + self._limit
        _limit = limit or self._limit
        return self._get_result(_offset, _limit)

    def prev_page(self, limit=None):
        _offset = self._offset - self._limit
        _offset = max(0, _offset)
        _limit = limit or self._limit
        return self._get_result(_offset, _limit)

    def _get_result(self, _offset, _limit):
        return get_query_result(self._api_instance, self._query_id, _offset, _limit)
