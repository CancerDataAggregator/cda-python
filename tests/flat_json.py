from cdapython import Q
from tests.global_settings import host,localhost


def test():
    q = Q('id = "TCGA-E2-A10A"')

    q1 = q.run(verbose=True, host=localhost,format="tsv")
    print(q1)


# print(q1.filter("id"))
# df = q1.to_dataframe()

# print(q1)

test()
