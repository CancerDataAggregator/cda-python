from cdapython import Q
from tests.global_settings import localhost


def testing():
    q = Q('id = "TCGA-E2-A10A"')

    r = q.(host=localhost)
    print(r.toDict))


testing()
