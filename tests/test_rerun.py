from cdapython import Q
from tests.global_settings import host

try:
    PDC = 'ResearchSubject.identifier.system = "PDC"'
    GDC = 'ResearchSubject.identifier.system = "GDC"'
    IDC = 'identifier.system = "IDC"'
    q1 = Q(PDC)
    q2 = Q(GDC)
    q3 = Q(IDC)

    q = q3.From(q1.From(q2))

    r = q.run(host=host, async_call=True)
    print(r)

    q1 = Q(PDC)
    q2 = Q(GDC)
    q3 = Q(IDC)

    q = q3.From(q1.From(q2))

    r = q.run(host=host, async_call=True)
    print(r)
    q1 = Q(PDC)
    q2 = Q(GDC)
    q3 = Q(IDC)

    q = q3.From(q1.From(q2))

    r = q.run(host=host, async_call=True)
    print(r)
except Exception as e:
    print(e)
