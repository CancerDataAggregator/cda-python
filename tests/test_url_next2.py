# pytest: skip
# This test file will be ignored by pytest
import pytest

from cdapython import Q, unique_terms
from tests.global_settings import localhost


@pytest.mark.skip(reason="currently total row count not being returned CD-610")
def test_total_count_for_subject_id():
    u_sex = unique_terms("subject_id").run(host=localhost)
    assert u_sex.total_row_count != 0
