import pytest

from cdapython import columns, unique_terms
from tests.global_settings import host


# @pytest.mark.skip(reason="currently total row count not being returned CD-610")
def test_gene_get_all():
    all_genes = unique_terms("Gene", "GCD").run(host=host).get_all(limit=2000)

    assert all_genes.total_row_count == len(all_genes)
