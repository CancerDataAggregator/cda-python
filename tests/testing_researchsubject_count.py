from cdapython import query, Q
from tests.global_settings import host


def testing_researchsubject() -> None:
    q2 = Q("sex = 'male'")
    q2.research_subject.count.run(host=host).pretty_print()


testing_researchsubject()
