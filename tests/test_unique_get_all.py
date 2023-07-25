from cdapython import columns, unique_terms
from tests.global_settings import host, project

# print(columns().to_list(filters="TP53"))
# df = (
#     unique_terms(
#         col_name="Gene",
#         show_counts=True,
#         host=integration_host,
#         table=integration_table,
#         page_size=1000,
#     )
#     .get_all()
#     .to_dataframe()
# )

# print(df[df["Gene"] == "Entrez_Gene_Id"])

all_genes = unique_terms("Gene", host=host, table=project).get_all(page_size=2000)

assert all_genes.total_row_count == len(all_genes)
