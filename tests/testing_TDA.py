from cdapython import Q
from tests.global_settings import host

# q1 = Q('subject_associated_project > "TCGA-OV"')


q1 = Q(
    "ResearchSubject.Diagnosis.Treatment QMath(days_treatment_end - days_to_treatment_start > 90)"
)
r = q1.run(host=host)
print(r)
# SELECT * FROM `gdc-bq-sample.integration.all_v2`,unnest(ResearchSubject) as RS, unnest(RS.Diagnosis) as D,
# unnest(D.Treatment) as T WHERE T.days_treatment_end - T.days_to_treatment_start > 90
q1 = Q('subject_associated_project = "TCGA-OV"')
r = q1.run(host=host)
print(r)
