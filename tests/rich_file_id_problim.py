from cdapython import Q, columns
from cdapython import unique_terms
from global_settings import host


def test():
    columns().to_list()

    columns().to_list(filters="primary_diagnosis_site")
    unique_terms("ResearchSubject.primary_diagnosis_site").to_list(filters="ov")

    r = Q("ResearchSubject.primary_diagnosis_site = 'Ovary'").file.run(host=host)
