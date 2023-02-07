from cdapython import Q, columns
from cdapython.functions import col
from cdapython.utility import unique_terms
from global_settings import localhost, host


def test():
    columns().to_list()

    columns().to_list(search_value="primary_diagnosis_site")
    unique_terms("ResearchSubject.primary_diagnosis_site").to_list(search_value="ov")

    r = Q("ResearchSubject.primary_diagnosis_site = 'Ovary'").file.run(host=host)
