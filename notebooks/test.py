# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # CDA Python: Features & Examples
# ---

# %%
from ipywidgets import Dropdown
from IPython.display import display

tester_check = Dropdown(
    options=[True, False],
    description="Tester:",
    value=True,
)
display(tester_check)

# %% [markdown]
# The following examples illustrate some ```CDA Python``` features while providing insights into the underlying data structure (**Getting started**). To demonstrate those features, we provide a few relevant text queries along with step-by-step explanations on how to translate those into the ```CDA Python``` queries (**Example queries**). Finally, there are a few additional queries intended for the test users to play around with and send feedback to the CDA team (**Test queries**).

# %%
from cdapython import Q, columns, unique_terms, query, constantVariables
import cdapython

print(cdapython.__file__)
print(cdapython.__version__)


# %%

if tester_check.value:
    Q.set_host_url("http://34.132.58.138:8080/")
else:
    Q.set_host_url("https://cda.cda-dev.broadinstitute.org")

print(Q.get_host_url())

# %% [markdown]
# ## Getting started
# %% [markdown]
# Print out the list of available fields with ```columns()```:

# %%
columns()

# %% [markdown]
# All of the above fields are what describes the highest entity in the data structure hierarchy – ```Patient``` entity. The first five fields represent ```Patient``` demographic information, while the ```ResearchSubject``` entity contains details that we are used to seeing within the nodes' ```Case``` record.
#
# One of the contributions of the CDA is aggregated ```ResearchSubject``` information. This means that all ```ResearchSubject``` records coming from the same subject are now gathered under the Patient entity. As we know, certain specimens are studied in multiple projects (being part of a single data node or multiple nodes) as different ```ResearchSubject``` entries. Those ```ResearchSubject``` entries are collected as a list under the ```ResearchSubject``` entity. One example of this is the patient record with ```id = TCGA-E2-A10A``` which contains two ```ResearchSubject``` entries, one from GDC and the other from PDC.
#
# Note that the ```ResearchSubject``` entity is a list of records, as many other entities above are. **There are certain considerations that should be made when creating the queries by using the fields that come from lists, but more about that will follow in examples below**.
#
# The names in the list may look familiar to you, but they may have been renamed or restructured in the CDA. The field name mappings are described in the _CDA Schema Field Mapping_ document that is linked in the _Testing Guide_. A more direct way to explore and understand the fields is to use the ```unique_terms()``` function:

# %%
unique_terms("ResearchSubject.Specimen.source_material_type", limit=10)

# %% [markdown]
# Additionally, you can specify a particular data node by using the ```system``` argument:

# %%
unique_terms("ResearchSubject.Specimen.source_material_type", system="PDC")

# %% [markdown]
# Now, let's dive into the querying!
#
# We can start by getting the record for ```id = TCGA-E2-A10A``` that we mentioned earlier:

# %%
q = Q('id = "TCGA-E2-A10A"')  # note the double quotes for the string value

r = q.run()


# %%


# %% [markdown]
# We see that we've got a single patient record as a result, which is what we expect.
#
# Let's see how the result looks like:

# %%
r[0]

# %% [markdown]
# The record is pretty large, so we'll print out ```identifier``` values for each ```ResearchSubject``` to confirm that we have one ```ResearchSubject``` that comes from GDC, and one that comes from PDC:

# %%
for research_subject in r[0]["ResearchSubject"]:
    print(research_subject["identifier"])

# %% [markdown]
# The values represent ```ResearchSubject``` IDs and are equivalent to ```case_id``` values in data nodes.
# %% [markdown]
# ## Example queries
# %% [markdown]
# Now that we can create a query with ```Q()``` function, let's see how we can combine multiple conditions.
#
# There are three operators available:
# * ```And()```
# * ```Or()```
# * ```From()```
#
# The following examples show how those operators work in practice.
# %% [markdown]
# ### Query 1
#
# **Find data for subjects who were diagnosed after the age of 50 and who were investigated as part of the TCGA-OV project.**

# %%
q1 = Q("ResearchSubject.Diagnosis.age_at_diagnosis > 50*365")
q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')

q = q1.And(q2)
r = q.run()

print(r)

# %% [markdown]
# ### Query 2
#
# **Find data for donors with melanoma (Nevi and Melanomas) diagnosis and who were diagnosed before the age of 30.**

# %%
q1 = Q('ResearchSubject.Specimen.primary_disease_type = "Nevi and Melanomas"')
q2 = Q("ResearchSubject.Diagnosis.age_at_diagnosis < 30*365")

q = q1.And(q2)
r = q.run()

print(r)

# %% [markdown]
# In addition, we can check how many records come from particular systems by adding one more condition to the query:

# %%
q1 = Q('ResearchSubject.Specimen.primary_disease_type = "Nevi and Melanomas"')
q2 = Q("ResearchSubject.Diagnosis.age_at_diagnosis < 30*365")
q3 = Q('ResearchSubject.Specimen.identifier.system = "GDC"')

q = q1.And(q2.And(q3))
r = q.run()

print(r)

# %% [markdown]
# By comparing the ```Count``` value of the two results we can see that all the patients returned in the initial query are coming from the GDC.
#
# To explore the results further, we can fetch the patient JSON objects by iterating through the results:

# %%
projects = set()

for patient in r:
    research_subjects = patient["ResearchSubject"]
    for rs in research_subjects:
        projects.add(rs["associated_project"])

print(projects)

# %% [markdown]
# The output shows the projects where _Nevi and Melanomas_ cases appear.
# %% [markdown]
# ### Query 3
#
# **Identify all samples that meet the following conditions:**
#
# * **Sample is from primary tumor**
# * **Disease is ovarian or breast cancer**
# * **Subjects are females under the age of 60 years**

# %%
tumor_type = Q('ResearchSubject.Specimen.source_material_type = "Primary Tumor"')
disease1 = Q('ResearchSubject.primary_disease_site = "Ovary"')
disease2 = Q('ResearchSubject.primary_disease_site = "Breast"')
demographics1 = Q('sex = "female"')
demographics2 = Q(
    "days_to_birth > -60*365"
)  # note that days_to_birth is a negative value

q1 = tumor_type.And(demographics1.And(demographics2))
q2 = disease1.Or(disease2)
q = q1.And(q2)

r = q.run()
print(r)

# %% [markdown]
# In this case, we have a result that contains more than 1000 records which is the default page size. To load the next 1000 records, we can use the ```next_page()``` method:

# %%
r2 = r.next_page()


# %%
print(r2)

# %% [markdown]
# Alternatively, we can use the ```offset``` argument to specify the record to start from:
#
# ```
# ...
# r = q.run(offset=1000)
# print(r)
# ```
# %% [markdown]
# ### Query 4
#
# **Find data for donors with "Ovarian Serous Cystadenocarcinoma" with proteomic and genomic data.**
# %% [markdown]
# **Note that disease type value denoting the same disease groups can be completely different within different systems. This is where CDA features come into play.** We first start by exploring the values available for this particular field in both systems.

# %%
unique_terms("ResearchSubject.primary_disease_type", system="GDC", limit=10)

# %% [markdown]
# Since “Ovarian Serous Cystadenocarcinoma” doesn’t appear in GDC values we decide to look into the PDC:

# %%
unique_terms("ResearchSubject.primary_disease_type", system="PDC")

# %% [markdown]
# After examining the output, we see that it does come from the PDC. Hence, if we could first identify the data that has research subjects found within the PDC that have this particular disease type, and then further narrow down the results to include only the portion of the data that is present in GDC, we could get the records that we are looking for.

# %%
q1 = Q('ResearchSubject.primary_disease_type = "Ovarian Serous Cystadenocarcinoma"')
q2 = Q('ResearchSubject.identifier.system = "PDC"')
q3 = Q('ResearchSubject.identifier.system = "GDC"')

q = q3.From(q1.And(q2))
r = q.run()

print(r)

# %% [markdown]
# As you can see, this is achieved by utilizing ```From``` operator. The ```From``` operator allows us to create queries from results of other queries. This is particularly useful when working with conditions that involve a single field which can take multiple different values for different items in a list that is being part of, e.g. we need ```ResearchSubject.identifier.system``` to be both “PDC” and “GDC” for a single patient. In such cases, ```And``` operator can’t help because it will return those entries where the field takes both values, which is zero entries.

# %%
for i in Q.sql(
    "SELECT * FROM `gdc-bq-sample.cda_mvp.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` WHERE table_name = 'v3' Limit 5"
):
    print(i)


# %%
q1 = query(
    'ResearchSubject.identifier.system = "GDC" FROM ResearchSubject.primary_disease_type = "Ovarian Serous Cystadenocarcinoma" AND ResearchSubject.identifier.system = "PDC"'
)
result = q1.run(async_call=True)
print(result)

# %% [markdown]
# ## Test queries
# %% [markdown]
# Now that we've successfully run and analyzed a few queries, here are a few additional ones you can try out on your own.
#
# Solutions can be shared with the CDA team as indicated in the _Testing Guide_ document.
# %% [markdown]
# ### Test Query 1
#
# **Find data from TCGA-BRCA project, with donors over the age of 50 with Stage IIIC cancer.**

# %%
# Solution

# ...

# print(r)

# %% [markdown]
# ### Test Query 2
#
# **Find data from all patients who have been treated with "Radiation Therapy, NOS" and have both genomic and proteomic data.**

# %%
# Solution

# ...

# print(r)

# %% [markdown]
# ### Test Query 3
#
# **Find data from all subjects with lung adenocarcinomas that have both primary and recurrent tumors.**

# %%
# Solution

# ...

# print(r)


# %%

Q('ResearchSubject.id = "c5421e34-e5c7-4ba5-aed9-146a5575fd8d"').run().pretty_print(-1)
