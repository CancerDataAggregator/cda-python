from cdapython import Q
from tests.global_settings import localhost, host

r = (
    Q("File.file_format = 'tsv'")
    .And(Q("ResearchSubject.Diagnosis.stage = 'Stage I' "))
    .Or(Q("ResearchSubject.Diagnosis.stage = 'Stage II'"))
    .And(Q("ResearchSubject.primary_diagnosis_site = 'Kidney'"))
)

q = r.research_subject
a = r.subject

x = q.run(host=host)
q2 = q.files.run(host=host)


print(x)
print(q2)
