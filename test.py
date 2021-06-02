from cdapython import Q, columns, unique_terms

qc2 = Q('ResearchSubject.Diagnosis.tumor_stage = "Stage IIIC" OR  ResearchSubject.Diagnosis.tumor_stage = "Stage IV" ')

dq1 = Q('ResearchSubject.Diagnosis.tumor_stage = "Stage IIIC" ')
dq2 = Q('ResearchSubject.Diagnosis.tumor_stage = "Stage IV" ')
q2 = dq1.Or(dq2)
r3 = q2.run(limit=1000) 
qc2.run()