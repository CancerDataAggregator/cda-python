from cdapython import Q
from tests.global_settings import localhost


def test():
    q = Q('id = "TCGA-E2-A10A"')

    # q1 = q.run(verbose=True, host=localhost, format_type="tsv")
    # check = q.run(verbose=True, host=localhost, format_type="tsv") == q.run(verbose=True, host=localhost, format_type="tsv")
    # q1 = q.run(verify=False, host=host)
    q1 = q.run(verbose=True, host=localhost, format_type="tsv")
    print(q1)


test()
