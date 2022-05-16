from cdapython.utility import unique_terms


def test_unique_terms_convert():
    d = unique_terms("ResearchSubject.associated_project")
    print(d)


test_unique_terms_convert()
