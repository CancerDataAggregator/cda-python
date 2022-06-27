from cdapython import Q
from tests.global_settings import localhost

r = (
    Q("ResearchSubject.Diagnosis.stage = 'Stage I'")
    .OR(Q("ResearchSubject.Diagnosis.stage = 'Stage II'"))
    .AND(Q('ResearchSubject.primary_diagnosis_site = "Breast Invasive Carcinoma"'))
)


print(r.to_json())
