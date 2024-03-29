from cdapython.Q import Q
from tests.global_settings import host, table

q1 = Q('primary_diagnosis_site = "Kidney"')
q2 = Q("stage = 'Stage I'")
q3 = Q("stage = 'Stage II'")
diag = q2.OR(q3)
myquery = diag.AND(q1)

count = myquery.count
file = myquery.file
file_count = file.count
subject = myquery.subject
rs = myquery.researchsubject
specimen = myquery.specimen
diagnosis = myquery.diagnosis
treatment = myquery.treatment


print(myquery.run(limit=500, host=host, table=table, async_call=True)[0])
print(subject.run(limit=500, host=host, table=table, async_call=True)[0])
print(subject.file.run(limit=500, host=host, table=table, async_call=True)[0])
print(subject.count.run(limit=500, host=host, table=table, async_call=True)[0])
print(subject.file.count.run(limit=500, host=host, table=table, async_call=True)[0])
print(rs.run(limit=500, host=host, table=table, async_call=True)[0])
print(rs.file.run(limit=500, host=host, table=table, async_call=True)[0])
print(rs.count.run(limit=500, host=host, table=table, async_call=True)[0])
print(rs.file.count.run(limit=500, host=host, table=table, async_call=True)[0])
print(specimen.run(limit=500, host=host, table=table, async_call=True)[0])
print(specimen.file.run(limit=500, host=host, table=table, async_call=True)[0])
print(specimen.count.run(limit=500, host=host, table=table, async_call=True)[0])
print(specimen.file.count.run(limit=500, host=host, table=table, async_call=True)[0])
print(diagnosis.run(limit=500, host=host, table=table, async_call=True)[0])
print(diagnosis.count.run(limit=500, host=host, table=table, async_call=True)[0])
print(treatment.run(limit=500, host=host, table=table, async_call=True))
print(treatment.count.run(limit=500, host=host, table=table, async_call=True)[0])
print(file.run(limit=500, host=host, table=table, async_call=True)[0])
print(count.run(limit=500, host=host, table=table, async_call=True)[0])
print(file_count.run(limit=500, host=host, table=table, async_call=True)[0])
