from cdapython import Q
from tests.global_settings import host, project


def testing():
    try:
        q = Q('subject_id = "TCGA-E2-A10A"')

        r = q.researchsubject.run(host=host, table=project)
        print(r.pretty_print())
    except Exception as e:
        print(e)
