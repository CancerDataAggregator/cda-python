from cdapython import Q, query
from tests.global_settings import host


def testing_like() -> None:
    q = query(
        'ResearchSubject.primary_disease_type LIKE "Lung_%" AND ResearchSubject.id = "P012"'
    )
    x = q.research_subject.run(host=host)
    print(x)
    v = Q('ResearchSubject.primary_disease_type = "Lung%"')
    r = v.subjects(host=host)
    print(r)


testing_like()
