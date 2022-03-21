from cdapython import Q
from tests.global_settings import host

try:
    q1 = Q('ResearchSubject.identifier.system = "PDC"')
    q2 = Q('ResearchSubject.identifier.system = "GDC"')
    q3 = Q('identifier.system = "IDC"')

    q = q3.From(q1.From(q2))

    r = q.run(host=host, async_call=True)
    print(r)

    q1 = Q('ResearchSubject.identifier.system = "PDC"')
    q2 = Q('ResearchSubject.identifier.system = "GDC"')
    q3 = Q('identifier.system = "IDC"')

    q = q3.From(q1.From(q2))

    r = q.run(host=host, async_call=True)
    print(r)
    q1 = Q('ResearchSubject.identifier.system = "PDC"')
    q2 = Q('ResearchSubject.identifier.system = "GDC"')
    q3 = Q('identifier.system = "IDC"')

    q = q3.From(q1.From(q2))

    r = q.run(host=host, async_call=True)
    print(r)
except Exception as e:
    print(e)
