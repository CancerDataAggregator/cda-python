from cdapython import unique_terms
from tests.global_settings import localhost


d = unique_terms(
    "ResearchSubject.Diagnosis",
    host="http://35.192.60.10:8080/",
    table="gdc-bq-sample.dev",
    show_sql=True,
    show_counts=True,
).to_dataframe()


print(d)
