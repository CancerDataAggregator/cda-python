from cdapython import Q
from tests.global_settings import host


q1 = Q(
    "ResearchSubject.Diagnosis.Treatment QMath(days_treatment_end - days_to_treatment_start > 90)"
)
r = q1.run(host=host)
print(r)
q1 = Q('subject_associated_project = "TCGA-OV"')
r = q1.run(host=host)
print(r)
