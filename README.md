# CDA Python

This library sits on top of the machine generated
[CDA Python Client](https://github.com/CancerDataAggregator/cda-service-python-client) and offers some syntactic
sugar to make it more pleasant to query the CDA.

# Launch in Binder

To try out the example notebook in [MyBinder.org](https://mybinder.org/)
without having to install anything, just click on the logo below. This will
launch a Jupyter Notebook instance with our example notebook ready to run.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CancerDataAggregator/cda-python/HEAD?filepath=example.ipynb)

# Runing CDA Python locally

Install the CDA Python library locally:

1. You need python3 installted
   - windows users and mac os users that don't want to use hombrew click on this [link](https://www.python.org/downloads/) or go to this website https://www.python.org/downloads/ and dowload python 3

`pip install git+https://github.com/CancerDataAggregator/cda-python.git`

# Basics

(Also see example [IPython notebook](example.ipynb))

```
from cdapython import Q, columns, unique_terms


columns() # List column names eg:
# ['days_to_birth',
#  'race',
#  'sex',
#  'ethnicity',
#  'id',
#  'ResearchSubject',
#  'ResearchSubject.Diagnosis',
#  'ResearchSubject.Diagnosis.morphology',
#  'ResearchSubject.Diagnosis.tumor_stage',
#  'ResearchSubject.Diagnosis.tumor_grade',
#  'ResearchSubject.Diagnosis.Treatment',
#  'ResearchSubject.Diagnosis.Treatment.type',
#  'ResearchSubject.Diagnosis.Treatment.outcome',


unique_terms("ResearchSubject.primary_disease_type") # List unique terms for this column eg:
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

print(r) # Prints some brief information about the result page eg:
#
# Query: SELECT * FROM gdc-bq-sample.cda_mvp.v1, UNNEST(ResearchSubject) AS _ResearchSubject WHERE (_ResearchSubject.# primary_disease_type = 'Adenomas and Adenocarcinomas')
# Offset: 0
# Limit: 2
# Count: 2
# More pages: Yes


r[0] # Returns nth result of this page as a Python dict e.g.
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


r.pretty_print(0) # Prints the nth result nicely
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

> Select data from TCGA-OV project, with donors over age 50

## Quick form

```
from cdapython import Q

q1 = Q('ResearchSubject.Diagnosis.age_at_diagnosis > 50*365')
q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')

q = q1.And(q2)
r = q.run()

print(r)

# Query: SELECT * FROM gdc-bq-sample.cda_mvp.v1, UNNEST(ResearchSubject) AS _ResearchSubject, UNNEST(_ResearchSubject.Diagnosis) AS # _Diagnosis WHERE ((_Diagnosis.age_at_diagnosis > 50*365) AND (_ResearchSubject.associated_project = 'TCGA-OV'))
# Offset: 0
# Limit: 1000
# Count: 461
# More pages: No

r.pretty_print(2)
# { 'Diagnosis': [ { 'Treatment': [ { 'outcome': None,
#                                     'type': 'Radiation Therapy, NOS'},
#                                   { 'outcome': None,
#                                     'type': 'Pharmaceutical Therapy, NOS'}],
#                    'age_at_diagnosis': 28779,
#                    'id': 'dc8af98b-03cb-5817-84fa-d86a7f2df8c6',
#                    'morphology': '8441/3',
#                    'primary_diagnosis': 'Serous cystadenocarcinoma, NOS',
#                    'tumor_grade': 'not reported',
#                    'tumor_stage': 'not reported'}],
#   'ResearchSubject': [ { 'Diagnosis': [ { 'Treatment': [ { 'outcome': None,
#                                                            'type': 'Radiation '
#                                                                    'Therapy, '
#                                                                    'NOS'},
#                                                          { 'outcome': None,
#                                                            'type': 'Pharmaceutical '
#                                                                    'Therapy, '
#                                                                    'NOS'}],
#                                           'age_at_diagnosis': 28779,
#                                           'id': 'dc8af98b-03cb-5817-84fa-d86a7f2df8c6',
#                                           'morphology': '8441/3',
#                                           'primary_diagnosis': 'Serous '
#                                                                'cystadenocarcinoma, '
#                                                                'NOS',
#                                           'tumor_grade': 'not reported',
#                                           'tumor_stage': 'not reported'}],
# ...

```

Any given part of a query is expressed as a string of three parts separated by spaces:

```
Q('esearchSubject.associated_project = "TCGA-OV"')
```

The first part is interpreted as a column name, the second as a comparator and
the third part as a value. If the value is a string, it needs to be put in
quotes.

## Detailed form

For cases where there may be ambiguity in the quoting, or the right side of the
comparison is another column, the detailed form should be used. Here the three
parts of a query are explicity split apart.

```
from cdapython import Q, Col, Quoted

q1 = Q(Col('ResearchSubject.Diagnosis.age_at_diagnosis'), '>=', 50 * 365)
q2 = Q(Col('ResearchSubject.associated_project'), '=', Quoted('TCGA-OV'))
```

# Pointing to a custom CDA instance

`.run()` will execute the query on the public CDA API (`https://cda.cda-dev.broadinstitute.org/api/cda/v1/`).

`.run("http://localhost:8080")` will execute the query on a CDA server running at
`http://localhost:8080`.

# Note

This is the spiritual successor of the
[Query Translator Prototype](https://github.com/CancerDataAggregator/translator-prototype)
