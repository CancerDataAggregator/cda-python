from cdapython import Q
from tests.global_settings import localhost


def testing():
    q = Q('id = "TCGA-E2-A10A"')

    r = q.research_subject(host=localhost)
    print(r.pretty_print())


testing()
