from cdapython import Q
from global_settings import integration_host, integration_table

a = (
    Q("subject_identifier_system = 'GDC'")
    .ORDER_BY("days_to_birth:-1")
    .subject.run(show_sql=True, host=integration_host, table=integration_table)
    .df_to_table()
)
print(a)

Q.bigquery_status()
