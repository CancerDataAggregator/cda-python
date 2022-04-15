from cdapython import query
from pandas import DataFrame, concat
from tests.global_settings import host

q = query('ResearchSubject.primary_disease_type LIKE "Lung%"').run(host=host)

df = DataFrame()
for i in q.paginator(to_df=True):
    print(len(i))
    df = concat([df, i])

print(df.head())
df.to_csv("test_data.tsv", sep="\t")
