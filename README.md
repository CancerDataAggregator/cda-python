# CDA Python
This library sits on top of the machine generated 
[CDA Python Client]() and offers some syntactic 
sugar to make it more pleasant to query the CDA.

# Install

`pip install git+https://github.com/CancerDataAggregator/cda-python.git`

# A simple query

> Select data from TCGA-OV project, with donors over age 50 with Stage IIIC cancer

```
from cdapython import Q

q1 = Q('demographic.age_at_index >= 50)
q2 = Q('project.project_id = "TCGA-OV"')
q3 = C('diagnoses.figo_stage = "Stage IIIC"')

q = q1.And(q2).And(q3)
print(q.sql())
rows = q.run()
```


This is the spiritual successor of the 
[Query Translator Prototype](https://github.com/CancerDataAggregator/translator-prototype)
