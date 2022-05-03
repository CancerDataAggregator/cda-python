from cdapython import Q, query
from tests.global_settings import host, localhost


def testing_like():
    q = query(
        'ResearchSubject.primary_disease_type LIKE "Lung_%" AND ResearchSubject.id = "P012"'
    )
    # print(q)
    # r = q.run(host="http://localhost:8080")
    # c = q.counts(host="http://localhost:8080")
    v = Q('ResearchSubject.primary_disease_type = "Lung%"')
    r = v.subjects(host=localhost)
    print(r)
    # print(r.pretty_print())


testing_like()
