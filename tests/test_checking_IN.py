from cdapython import Q
from tests.global_settings import host


def checking_test():
    q1 = Q(
        "ResearchSubject.id IN ['4da7abaf-ac7a-41c0-8033-5780a398545c','010df72d-63d9-11e8-bcf1-0a2705229b82']"
    )
    print(q1)
    assert q1.query.to_dict()["node_type"] == "IN"
    r = q1.run(host=host)


checking_test()
