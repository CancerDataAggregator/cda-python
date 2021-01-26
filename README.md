# CDA Python
This library sits on top of the machine generated 
[CDA Python Client](https://github.com/CancerDataAggregator/cda-service-python-client) and offers some syntactic 
sugar to make it more pleasant to query the CDA.

# Install

`pip install git+https://github.com/CancerDataAggregator/cda-python.git`

# A simple query

> Select data from TCGA-OV project, with donors over age 50 with Stage IIIC cancer

## Quick form
```
from cdapython import Q

q1 = Q('demographic.age_at_index >= 50')
q2 = Q('project.project_id = "TCGA-OV"')
q3 = Q('diagnoses.figo_stage = "Stage IIIC"')

q = q1.And(q2).And(q3)
print(q.sql())
rows = q.run()
```

Any given part of a query is expressed as a string of three parts separated by spaces:
```
Q('project.project_id = "TCGA-OV"')
```
The first part is interpreted as a column name, the second as a comparator and
the third part as a value. If the value is a string, it needs to be put in
quotes.

A query can be executed (`.run()`) or the generated SQL inspected (`.sql()`)


## Detailed form

For cases where there may be ambiguity in the quoting, or the right side of the
comparison is another column, the detailed form should be used. Here the three
parts of a query are explicity split apart.

```
from cdapython import Q, Col, Quoted
q3 = Q(Col('diagnoses.figo_stage), "=", Quoted('Stage IIIC'))
```


# Pointing to a custom CDA instance

`.run()` will execute the query on the public CDA API on the 

`.run("http://localhost:8080")` will execute the query on a CDA server running at
`http://localhost:8080`.  


# Note

This is the spiritual successor of the 
[Query Translator Prototype](https://github.com/CancerDataAggregator/translator-prototype)
