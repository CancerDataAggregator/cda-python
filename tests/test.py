from cdapython import Q
from time import time
from pandas import DataFrame

data = {"parse1": [], "parse2": []}
for i in range(1000):
    start = int(round(time() * 1000))
    Q(
        "stage = 'Stage I' OR stage = 'Stage II' AND primary_diagnosis_site = 'Kidney' AND subject_associated_project = 'CPTAC-3' AND file_format = 'tsv'"
    ).to_json()
    end = int(round(time() * 1000))
    start_a = int(round(time() * 1000))
    q1 = Q('primary_diagnosis_site = "Kidney"')
    q2 = Q("stage = 'Stage I'")
    q3 = Q("stage = 'Stage II'")
    diag = q2.OR(q3)
    myquery = diag.AND(q1)
    myquery.AND(Q("subject_associated_project = 'CPTAC-3'")).AND(
        Q("file_format = 'tsv'")
    ).to_json()
    end_a = int(round(time() * 1000))

    data["parse1"].append(round(end - start))
    data["parse2"].append(round(end_a - start_a))


df = DataFrame(data)
print(df.describe())
