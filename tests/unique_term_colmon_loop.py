from cdapython import columns, unique_terms
from tests.global_settings import localhost, integration_host

databases = "gdc-bq-sample.dev"
allcolumns = columns().to_list()


for i in allcolumns:
    try:
        temp = unique_terms(i, show_sql=True)
        if temp.to_list(filters="slide"):
            print(i)
    except:
        pass
