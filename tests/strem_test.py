from cdapython import query
from pandas import DataFrame, concat
from tests.global_settings import host, localhost

q = query('ResearchSubject.primary_disease_type LIKE "Lung%"').run(host=localhost)

df = DataFrame()
for i in q.paginator(to_df=True):
    df = concat([df, i])

print(df.head())
print(len(df))
df.to_csv("test_data.tsv", sep="\t")
