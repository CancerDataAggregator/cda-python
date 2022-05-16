from cdapython import Q, columns
from cdapython.utility import unique_terms
from tests.global_settings import localhost

# q = Q('id != "TCGA-13-1409"').run()
# print(q.to_list())  # note the double quotes for the string value
# print(q.to_dataframe())
# print(columns(host=localhost))
print(columns(host=localhost).to_dataframe())
print(unique_terms("ResearchSubject.Diagnosis.stage", host=localhost, show_sql=True))
# print(columns(host=localhost))
# r = q.run(host=localhost, verbose=False)
# df = r.to_dataframe()
# print(r)
# print(df.info())
# print(df.head())

# r.to_dataframe().to_csv("test.tsv", sep="\t")
