from cdapython import Q, query
from tests.global_settings import host, localhost


def testing_like():
    q = query(
        'ResearchSubject.primary_disease_type LIKE "Lung_%" AND ResearchSubject.id = "P012"'
    )
    x = q.research_subject.run(host=localhost)
    print(x)
    v = Q('ResearchSubject.primary_disease_type = "Lung%"')
    r = v.subjects(host=localhost)
    print(r)


testing_like()
