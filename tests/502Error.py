import json

from cdapython import Q

q1 = Q("ResearchSubject.Diagnosis.age_at_diagnosis > 50*365")
q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')
q = q1.And(q2)

data = q.file.run(host="http://localhost:8080")

open("test.json", "a+").write(json.dumps(data[0], indent=4))
