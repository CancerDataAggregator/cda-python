from pandas import DataFrame, concat

from cdapython import query
from tests.global_settings import host, localhost

q = query('ResearchSubject.primary_disease_type LIKE "Lung%"').run(host=host)

box = []
for i in q.paginator(to_list=True):
    box.extend(i)

print(len(box))
