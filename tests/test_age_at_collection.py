from cdapython import Q
from tests.global_settings import host, table

p = Q("ResearchSubject.Specimen.age_at_collection <= 10")
print(p)

print(p.specimen.run(host=host, table=table).to_dataframe())
