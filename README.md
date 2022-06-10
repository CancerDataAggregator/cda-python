# CDA Python

This library sits on top of the machine generated
[CDA Python Client](https://github.com/CancerDataAggregator/cda-service-python-client) and offers some syntactic
sugar to make it more pleasant to query the CDA.

---
## Read The Docs
[CDA Read The Docs](https://cda.readthedocs.io/en/latest/)

---
# Launch in Binder

To try out the example notebook in [MyBinder.org](https://mybinder.org/)
without having to install anything, just click on the logo below. This will
launch a Jupyter Notebook instance with our example notebook ready to run.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CancerDataAggregator/cda-python/HEAD?filepath=/notebooks/example.ipynb)

## For Testers use this Binder

Click on the logo below. This will
launch a Jupyter Notebook instance with our example notebook ready to run.

[![MyBinder.org](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CancerDataAggregator/cda-python/integration)

Install the CDA Python library locally:

1. Download and install docker click this [link](https://www.docker.com/products/docker-desktop) or copy url https://www.docker.com/products/docker-desktop to your Browser
2. Open Terminal or PowerShell a and navigate to cda-python folder then we will run a docker command
   - `docker compose up --build`
3. Open a Browser to this url http://localhost:8888 and you are up and running.

   - **To change the Port** edit the `.env` file NOTEBOOK_PORT

4. To Stop the container from running return to the terminal where the cdapython project is on your keyboard you will click **Control C to stop** the container .

To delete the container use this command in the cdapython project directory.

- `docker compose down`

### Pip install

Alternatively, CDA Python can be installed using `pip`. However, this requires python >= 3.6 on your system. To check your version at the command-line run `python -V`. To update your version you can download from [https://www.python.org/downloads/]('https://www.python.org/downloads/') additional python installation help can be found [here]('https://realpython.com/installing-python/'). Once you have the proper python version, you can run CDA using:

`pip install git+https://github.com/CancerDataAggregator/cda-python.git`

**NOTE: We recommend the docker method because pip installation can be a bit more cumbersome, and will not be as closely monitored as the docker installation.**

# Basics

We will now show you the basic structure of `CDA python` through the use of the most commands:

- `columns()`: show all available columns in the table,
- `unique_terms()`: for a given column show all unique terms,
- `Q`: Executes this query on the public CDA server, and
- `Q.sql`: allows you to enter SQL style queries.
- `query` : allows you to write long form Q statments with out chaining

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

r1 = Q.sql("""
SELECT
*
FROM gdc-bq-sample.cda_mvp.v1, UNNEST(ResearchSubject) AS _ResearchSubject
WHERE (_ResearchSubject.primary_disease_type = 'Adenomas and Adenocarcinomas')
""")

r1.pretty_print(0)
#
#{ 'Diagnosis': [],
#  'ResearchSubject': [ { 'Diagnosis': [],
#                         'Specimen': [],
#                         'associated_project': 'CGCI-HTMCP-CC',
#                         'id': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3',
#                         'identifier': [ { 'system': 'GDC',
#                                           'value': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3'}],
#                         'primary_disease_site': 'Cervix uteri',
#                         'primary_disease_type': 'Adenomas and '
#                                                 'Adenocarcinomas'}],
#  'Specimen': [],
#  'associated_project': 'CGCI-HTMCP-CC',
#  'days_to_birth': None,
#  'ethnicity': None,
#  'id': 'HTMCP-03-06-02177',
#  'id_1': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3',
#  'identifier': [ { 'system': 'GDC',
#                    'value': '4d54f72c-e8ac-44a7-8ab9-9f20001750b3'}],
#  'primary_disease_site': 'Cervix uteri',
#  'primary_disease_type': 'Adenomas and Adenocarcinomas',
#  'race': None,
#  'sex': None}


query('ResearchSubject.identifier.system = "GDC" FROM ResearchSubject.primary_disease_type = "Ovarian Serous Cystadenocarcinoma" AND ResearchSubject.identifier.system = "PDC"')
result = q1.run()
```

# Comparison operators

The following comparsion operators can be used with the `Q` command:

| operator | Description                                        | Q.sql required? |
| -------- | -------------------------------------------------- | --------------- |
| =        | condition equals                                   | no              |
| !=       | condition is not equal                             | no              |
| <        | condition is less than                             | no              |
| >        | condition is greater than                          | no              |
| <=       | condition is less than or equal to                 | no              |
| >=       | condition is less than or equal to                 | no              |
| like     | similar to = but always wildcards ('%', '\_', etc) | yes             |
| in       | compares to a set                                  | yes             |

additionally, more complex SQL can be used with the `Q.sql` command.

# A simple query

> Select data from TCGA-OV project, with donors over age 50

## Quick form

```
from cdapython import Q

q1 = Q('ResearchSubject.Diagnosis.age_at_diagnosis > 50*365')
q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')

q = q1.AND(q2)
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
Q('ResearchSubject.associated_project = "TCGA-OV"')
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

# Quick Explanation on UNNEST usage in BigQuery

Using Q in the CDA client will echo the generated SQL statement that may contain multiple `UNNEST` inclusions
when including a dot(.) structure which may need a quick explanation.
UNNEST is similar to unwind in which embedded data structures must be flattend to appear in a table or Excel file.
Note; The following call using the SQL endpoint is not the preferred method to execute a nested attribute query in BigQuery.
The Q language DSL abstracts the required unnesting that exists in a Record. In BigQuery, structures must be represented in an UNNEST syntax such that:
`A.B.C.D` must be unwound to `SELECT (_C.D)` in the following fashion:

```
SELECT (_C.D)
from TABLE, UNNEST(A) AS _A, UNNEST(_A.B) as _B, UNNEST(_B.C) as _C
```

`ResearchSubject.Specimen.source_material_type` represents a complex record that needs to unwound in SQL syntax to be queried on properly when using SQL.

```
SELECT DISTINCT(_Specimen.source_material_type)
FROM gdc-bq-sample.cda_mvp.v3,
UNNEST(ResearchSubject) AS _ResearchSubject,
UNNEST(_ResearchSubject.Specimen) AS _Specimen
```

# Developer setup
Python 3.7 or higher installed

git clone the repo

``` bash
git clone https://github.com/CancerDataAggregator/cda-python.git
```


open a terminal or powershell and navigate to cloned directory

example:

``` bash
cd cda-python
````

in the cda-python folder create a virtual environment
using

```python
python3 -m venv venv
```

and activate the environment by using
for the mac and push enter
```bash
source ./venv/bin/activate
```
and for windows in powershell and push enter
```
.\venv\Scripts\activate
```
note to stop using venv type
```bash
deactivate
```
### Project dependencies
In your virtual environment install  project requirements
Use pip to install the Python dependencies:
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Using pip-tools
In your virtual environment install
```bash
pip install pip-tools
```
we will use pip-tools to keep track of our dependencies and our requirements.in

Commands
```bash
pip-compile
 ```
will build requirements.txt from our setup.py and requirements.in and lockdown the requirements.txt

### Update requirements
just add dependency to the requirements.in and run
```bash
pip-compile
```
## cdapython local dev
to install the cdapython Library when you are working on the package locally as a dev
make sure you are in the main cdapython folder from you git clone and in your terminal
navigate to the folder then use `ls` or `DIR` to see the files make sure you see the setup.py file.
the setup.py file is used to tell pip
-e editable install so yo can update files
`pip install -e .`
## Note For runing pytest
there is a global_setting.py here you can change the host server




# Note

This is the spiritual successor of the
[Query Translator Prototype](https://github.com/CancerDataAggregator/translator-prototype)
