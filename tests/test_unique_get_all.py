import pytest

from cdapython import columns, unique_terms
from tests.global_settings import host, project

# print(columns().to_list(filters="TP53"))
# df = (
#     unique_terms(
#         col_name="Gene",
#         show_counts=True,
#         host=integration_host,
#         table=integration_table,
#         limit=1000,
#     )
#     .get_all()
#     .to_dataframe()
# )


# print(df[df["Gene"] == "Entrez_Gene_Id"])


@pytest.mark.skip(reason="currently total row count not being returned CD-610")
def test_gene_get_all():
    all_genes = unique_terms("Gene").run().get_all(limit=2000)

    assert all_genes.total_row_count == len(all_genes)
