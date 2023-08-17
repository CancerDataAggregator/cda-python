from global_settings import integration_host, integration_table

from cdapython import Q

r = Q("file_format = 'tsv'").AND(Q("SYMBOL LIKE 'TP53%'"))

# q = r.research_subject
# a = r.subject

# x = q.run(host=host)
q2 = r.file.run(show_sql=True, host=integration_host, table=integration_table)

q3 = r.file.run(show_sql=True)


# print(x)

assert q2.total_row_count == q3.total_row_count
