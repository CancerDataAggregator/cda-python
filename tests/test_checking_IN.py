from cdapython import Q
from tests.global_settings import host


def checking_test():
    q1 = Q(
        "ResearchSubject.id IN ['C0EF0C13-3109-47CF-9BA4-076AB7EB7660',' 6AA44F89-FCE7-46FE-A1CB-874CD5EFA4A4']"
    ).And(Q('sex = "male"'))
    print(q1)
    assert q1.query.to_dict()["node_type"] == "IN"
    r = q1.run(host=host)


checking_test()
