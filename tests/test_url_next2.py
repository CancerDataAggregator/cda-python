import pytest

from cdapython import Q, unique_terms
from tests.global_settings import host


def test_total_count_for_subject_id():
    u_sex = unique_terms("subject_id", host=host)
    assert u_sex.total_row_count != 0
