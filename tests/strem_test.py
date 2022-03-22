from cdapython import query
from pandas import DataFrame,concat

q = query('ResearchSubject.primary_disease_type LIKE "Lung%"').run(host="http://localhost:8080")


# df = r.to_dataframe()
# while r.has_next_page:
#     print(r)
#     r = r.next_page()
#     df = pd.concat([df, r.to_dataframe()])

df = DataFrame()
for i in q.paginator(to_df=True):
    print(len(i))
    df = concat([df,i])

print(df.head())
df.to_csv("test_data.tsv",sep="\t")

