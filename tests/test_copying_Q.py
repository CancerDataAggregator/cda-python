from cdapython import Q
from tests.global_settings import localhost, host

def test_copying_Q():

    q1 = Q('ResearchSubject.primary_disease_type = "Lung%"')

    q1.subject.run(host=host)
    q1.file.run(host=host)
