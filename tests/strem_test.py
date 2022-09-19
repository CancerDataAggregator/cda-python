from pandas import DataFrame, concat

from cdapython import Q
from tests.global_settings import host, localhost, table, table_dev, dev_host

q = Q('primary_disease_type LIKE "Lung%"').run(host=dev_host, table=table_dev)

print(q)
box = []
for i in q.paginator(to_list=True):
    box.extend(i)

print(len(box))
