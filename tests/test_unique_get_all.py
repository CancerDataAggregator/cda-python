from cdapython import unique_terms
from tests.global_settings import host


def test_gene_get_all():
    genes = unique_terms("Gene").run(host=host, limit=100)
    assert len(genes.to_dataframe()) == 100

    all_genes = genes.get_all(limit=2000)

    assert all_genes.total_row_count == len(all_genes)
