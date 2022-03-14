from memory_profiler import profile
from cdapython import Q,query


@profile
def testing_like():
    q = query('ResearchSubject.primary_disease_type LIKE "Lung%" AND ResearchSubject.id = "P012"')
    print(q)
    r = q.run(host="http://localhost:8080")
    c = q.counts(host="http://localhost:8080")

    print(r)


testing_like()
