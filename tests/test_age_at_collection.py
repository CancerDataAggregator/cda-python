from cdapython import Q
from tests.global_settings import host

p = Q("ResearchSubject.Specimen.age_at_collection <= 10")
print(p)

print(p.specimen.run(host=host).to_dataframe())
