from memory_profiler import profile
from cdapython import Q
from tests.global_settings import host

@profile
def test():
    q = Q('id = "TCGA-E2-A10A"')

    q1 = q.run(verbose=True, host=host, filter="id")
    print(q1)


# print(q1.filter("id"))
# df = q1.to_DataFrame()

# print(q1)

test()
