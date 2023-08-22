from global_settings import integration_host, integration_table

from cdapython import Q
from cdapython.utils.utility import unique_terms

r = Q(
    """
    primary_disease_type LIKE '%Carcinoma%' 
    AND file_format = 'tsv' 
    OR file_format = 'BAM'
    """
)

# q = r.research_subject
# a = r.subject


print(unique_terms("primary_disease_type").to_dataframe())
# # x = q.run(host=host)
q2 = r.treatment.run(show_sql=True, host=integration_host, table=integration_table)

q3 = r.treatment.run(show_sql=True)


print(q2)
print(q3)
# print(x)

assert q2.total_row_count == q3.total_row_count
