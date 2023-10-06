from global_settings import integration_host, integration_table
from pandas import DataFrame, concat

from cdapython import Q

df = DataFrame()
for i in (
    Q("subject_identifier_system = 'GDC'")
    .ORDER_BY("days_to_birth:-1")
    .subject.run(show_sql=True, host=integration_host, table=integration_table)
    .paginator(limit=8000, to_df=True)
):
    df = concat([i, df])


print(df)
# Q.bigquery_status()
