from cdapython import unique_terms
from tests.global_settings import host


def test_unique_terms_convert() -> None:
    d = unique_terms("ResearchSubject.associated_project", host=host)
    print(d)


test_unique_terms_convert()
