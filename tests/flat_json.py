from cdapython import Q
from tests.global_settings import localhost


def test():
    q = Q('id = "TCGA-E2-A10A"')
    print()

    # q1 = q.run(verbose=True, host=localhost, format_type="tsv")
    # check = q.run(verbose=True, host=localhost, format_type="tsv") == q.run(verbose=True, host=localhost, format_type="tsv")
    # q1 = q.run(verify=False, host=host)
    q1 = q.run(verbose=True, host=localhost, format="tsv")
    print(q1)
    for i in q1:
        print(i)
    print(q1.to_dataframe().head())


test()
