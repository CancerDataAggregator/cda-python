from cdapython import Q
from tests.global_settings import host, table


def testing():
    try:
        q = Q('id = "TCGA-E2-A10A"')

        r = q.researchsubject.run(host=host, table=table)
        print(r.pretty_print())
    except Exception as e:
        print(e)
