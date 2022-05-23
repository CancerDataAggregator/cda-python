from cdapython import query, Q
from tests.global_settings import host


def testing_subject() -> None:
    q2 = Q("sex = 'male'")
    print(q2.to_json())

    q2.subject.count.run(host=host).pretty_print()
