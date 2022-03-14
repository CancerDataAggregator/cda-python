from memory_profiler import profile
from cdapython import Q


@profile
def test():
    q = Q('id = "TCGA-E2-A10A"')

    q1 = q.run(verbose=True, host="http://localhost:8080", filter="id")
    print(q1)


# print(q1.filter("id"))
# df = q1.to_DataFrame()

# print(q1)

test()
