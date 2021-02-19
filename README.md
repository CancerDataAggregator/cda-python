# CDA Python
This library sits on top of the machine generated 
[CDA Python Client](https://github.com/CancerDataAggregator/cda-service-python-client) and offers some syntactic 
sugar to make it more pleasant to query the CDA.

# Install

`pip install git+https://github.com/CancerDataAggregator/cda-python.git`

# Basics

```
from cdapython import Q, unique_terms


unique_terms("ResearchSubject.primary_disease_type")

# Results in a list of unique terms for this column eg:
# [None,
#  'Acinar Cell Neoplasms',
#  'Adenomas and Adenocarcinomas',
#  'Adnexal and Skin Appendage Neoplasms',
#  'Basal Cell Neoplasms',
#  'Blood Vessel Tumors',
#  'Breast Invasive Carcinoma',
#  'Chromophobe Renal Cell Carcinoma',
#  'Chronic Myeloproliferative Disorders',
#  'Clear Cell Renal Cell Carcinoma',
#  'Colon Adenocarcinoma',
# ...

q1 = Q('ResearchSubject.primary_disease_type = "Adenomas and Adenocarcinomas"')
r = q1.run()                                 # Executes this query on the public CDA server
# r = q1.run(host="http://localhost:8080")   # Executes on local instance of CDA server
# r = q1.run(limit=2)                        # Limit to two results per page


r.sql   # Return SQL string used to generate the query e.g.
# "SELECT * FROM gdc-bq-sample.cda_mvp.v1, UNNEST(ResearchSubject) AS _ResearchSubject WHERE (_ResearchSubject.primary_disease_type = 'Adenomas and Adenocarcinomas')"

print(r)

# Prints some brief information about the result page eg:
#
# Query: SELECT * FROM gdc-bq-sample.cda_mvp.v1, UNNEST(ResearchSubject) AS _ResearchSubject WHERE (_ResearchSubject.# primary_disease_type = 'Adenomas and Adenocarcinomas')
# Offset: 0
# Limit: 2
# Count: 2
# More pages: Yes


r[0]  

# Returns nth result of this page as a Python dict e.g.
#
# {'days_to_birth': None,
#  'race': None,
#  'sex': None,
#  'ethnicity': None,
#  'id': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3',
#  'ResearchSubject': [{'Diagnosis': [],
#    'Specimen': [],
#    'associated_project': 'CGCI-HTMCP-CC',
#    'id': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3',
#    'primary_disease_type': 'Adenomas and Adenocarcinomas',
#    'identifier': [{'system': 'GDC',
#      'value': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3'}],
#    'primary_disease_site': 'Cervix uteri'}],
#  'Diagnosis': [],
#  'Specimen': [],
#  'associated_project': 'CGCI-HTMCP-CC',
#  'primary_disease_type': 'Adenomas and Adenocarcinomas',
#  'identifier': [{'system': 'GDC',
#    'value': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3'}],
#  'primary_disease_site': 'Cervix uteri'}


r.pretty_print(0)

# Prints the nth result nicely
#
# { 'Diagnosis': [],
#   'ResearchSubject': [ { 'Diagnosis': [],
#                          'Specimen': [],
#                          'associated_project': 'CGCI-HTMCP-CC',
#                          'id': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3',
#                          'identifier': [ { 'system': 'GDC',
#                                            'value': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3'}],
#                          'primary_disease_site': 'Cervix uteri',
#                          'primary_disease_type': 'Adenomas and '
#                                                  'Adenocarcinomas'}],
#   'Specimen': [],
#   'associated_project': 'CGCI-HTMCP-CC',
#   'days_to_birth': None,
#   'ethnicity': None,
#   'id': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3',
#   'identifier': [ { 'system': 'GDC',
#                     'value': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3'}],
#   'primary_disease_site': 'Cervix uteri',
#   'primary_disease_type': 'Adenomas and Adenocarcinomas',
#   'race': None,
#   'sex': None}


r2 = r.next_page()  # Fetches the next page of results 

print(r2)

# Query: SELECT * FROM gdc-bq-sample.cda_mvp.v1, UNNEST(ResearchSubject) AS _ResearchSubject WHERE (_ResearchSubject.# primary_disease_type = 'Adenomas and Adenocarcinomas')
# Offset: 2
# Limit: 2
# Count: 2
# More pages: Yes
```



# A simple query

> Select data from TCGA-OV project, with donors over age 50 with Stage IIIC cancer

## Quick form
```
from cdapython import Q

q1 = Q('Diagnosis.age_at_diagnosis >= 50')
q2 = Q('Specimen.associated_project = "TCGA-OV"')
q3 = Q('Diagnosis.tumor_stage = "Stage IIIC"')

q = q1.And(q2).And(q3)
response = q.run()

response.query_sql # Gives the SQL executed
response.result[0] # Gives first row of result as a Python dict
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

q1 = Q(Col('Diagnosis.age_at_diagnosis'), '>=', 50)
q3 = Q(Col('Diagnosis.tumor_stage), "=", Quoted('Stage IIIC'))
```


# Pointing to a custom CDA instance

`.run()` will execute the query on the public CDA API (`https://cda.cda-dev.broadinstitute.org/api/cda/v1/`).

`.run("http://localhost:8080")` will execute the query on a CDA server running at
`http://localhost:8080`.  


# Note

This is the spiritual successor of the 
[Query Translator Prototype](https://github.com/CancerDataAggregator/translator-prototype)
